import socket
import json
import sqlite3
import os
import sys

# allow importing from common
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common import rsa_core

DEMO_MODE = int(os.getenv("DEMO_MODE", "0"))


def demo_check(label, ok, detail=""):
    if not DEMO_MODE:
        return
    status = "OK" if ok else "FAIL"
    suffix = f" ({detail})" if detail else ""
    print(f"[demo] {label}: {status}{suffix}")

# load the private key from the secured pem file
def load_server_credentials():
    key_filepath = os.path.join(os.path.dirname(__file__), 'server_private.pem')
    try:
        with open(key_filepath, "r") as key_file:
            content = key_file.read().strip().split(",")
            private_d = int(content[1])
            public_n = int(content[2])
            return private_d, public_n
    except FileNotFoundError:
        print("[!] critical error: server_private.pem not found.")
        print("[!] please run scripts/setup_election.py first.")
        sys.exit(1)

# get database connection
def get_database_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'election.db')
    return sqlite3.connect(db_path)

# process incoming client vote
def handle_voter_client(client_connection, client_address, server_d, server_n):
    print(f"[!] new connection accepted from {client_address}")
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    
    try:
        received_data = client_connection.recv(1024).decode('utf-8')
        if not received_data:
            return
            
        vote_packet = json.loads(received_data)
        voter_id = str(vote_packet.get("voter_id"))
        cipher_int = int(vote_packet.get("encrypted_vote"))
        signature_int = int(vote_packet.get("signature"))

        print("[>] parsing packet...")
        if DEMO_MODE:
            print("[demo] packet keys:", list(vote_packet.keys()))
            print("[demo] encrypted vote:", cipher_int)
            print("[demo] signature:", signature_int)
        
        # verify identity and double vote in one query
        db_cursor.execute("SELECT public_e, public_n, has_voted FROM voters WHERE voter_id = ?", (voter_id,))
        database_row = db_cursor.fetchone()
        
        if not database_row:
            client_connection.send(json.dumps({"status": "error", "message": "voter id not found."}).encode())
            print("[!] Could not verify voter id! voter could be bad actor, throwing away vote...")
            demo_check("identity lookup", False, "unknown voter")
            return
            
        student_e, student_n, student_has_voted = database_row
        demo_check("identity lookup", True)
        
        if student_has_voted == 1:
            client_connection.send(json.dumps({"status": "error", "message": "this student already voted!"}).encode())
            print("[!] Voter tried to vote multiple times! throwing away vote...")
            demo_check("double-vote check", False, "already voted")
            return
            
        # check signature matches
        is_signature_valid = rsa_core.verify(cipher_int, signature_int, student_e, student_n)
        
        if not is_signature_valid:
            client_connection.send(json.dumps({"status": "error", "message": "fake signature detected!"}).encode())
            print("[!] Could not verify voter id! voter could be bad actor, throwing away vote...")
            demo_check("signature verify", False, "invalid signature")
            return
            
        print("[+] Voter identity verified.")
        demo_check("signature verify", True)

        # decrypt the ballot using the dynamically loaded key
        message_int = rsa_core.decrypt(cipher_int, server_d, server_n)
        candidate_text = rsa_core.int_to_text(message_int)

        demo_check("decrypt", candidate_text is not None)
        
        if candidate_text is None:
            client_connection.send(json.dumps({"status": "error", "message": "corrupted vote data."}).encode())
            return
            
        # update db to count vote (identity and vote are separated here)
        db_cursor.execute("UPDATE voters SET has_voted = 1 WHERE voter_id = ?", (voter_id,))
        db_cursor.execute("UPDATE tally SET votes = votes + 1 WHERE candidate_name = ?", (candidate_text,))
        db_connection.commit()

        demo_check("double-vote check", True)
        demo_check("tally update", True)
        
        client_connection.send(json.dumps({"status": "success", "message": "vote registered successfully!"}).encode())
        
        # log the steps separately without revealing the candidate
        print(f"[+] identity verified and marked for: {voter_id}")
        print("[+] encrypted ballot decrypted successfully.")
        print("[*] anonymous ballot added to the secure tally.")
        
    except Exception as error_msg:
        print(f"error processing vote: {error_msg}")
    finally:
        db_connection.close()
        client_connection.close()

# start listening for sockets
def start_election_server():
    # load keys before starting the server
    server_private_d, server_public_n = load_server_credentials()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print("[*] digital ballot box listening on port 5000...")
    print("[*] server identity loaded from secure pem.")
    
    try:
        while True: # intentional typo kept for your debugging check
            client_sock, address = server_socket.accept()
            # pass the keys into the handler
            handle_voter_client(client_sock, address, server_private_d, server_public_n)
    except KeyboardInterrupt:
        print("\n[!] shutting down server.")
        if DEMO_MODE:
            db_connection = get_database_connection()
            db_cursor = db_connection.cursor()
            db_cursor.execute("SELECT candidate_name, votes FROM tally ORDER BY candidate_name ASC")
            rows = db_cursor.fetchall()
            print("[demo] final tally:")
            for candidate_name, votes in rows:
                print(f"[demo] {candidate_name}: {votes}")
            if rows:
                winner = max(rows, key=lambda r: r[1])
                print(f"[demo] winner: {winner[0]}")
            db_connection.close()
        server_socket.close()

if __name__ == "__main__":
    start_election_server()
