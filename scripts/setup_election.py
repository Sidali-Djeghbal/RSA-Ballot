import sqlite3
import os
import random
import sys

# add root folder to path so we can import common
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# greatest common divisor
def calculate_gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# extended euclidean logic
def find_mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    return None

# check if number is prime
def is_prime(number):
    if number < 2: return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

# prepare the sqlite tables
def setup_database():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'election.db')
    connection = sqlite3.connect(db_path)
    db_cursor = connection.cursor()
    
    # create voters table
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS voters (
            voter_id TEXT PRIMARY KEY,
            public_e INTEGER,
            public_n INTEGER,
            has_voted INTEGER DEFAULT 0
        )
    ''')
    
    # create tally table
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS tally (
            candidate_name TEXT PRIMARY KEY,
            votes INTEGER DEFAULT 0
        )
    ''')
    
    candidates_list = ["Candidate A", "Candidate B", "Candidate C"]
    for candidate in candidates_list:
        db_cursor.execute('INSERT OR IGNORE INTO tally (candidate_name, votes) VALUES (?, 0)', (candidate,))
        
    connection.commit()
    return connection

# generate the master key for the ballot box
def generate_server_key():
    # we use specific primes here so the client's hardcoded public key stays valid
    prime_p, prime_q = 239, 263
    modulus_n = prime_p * prime_q
    public_e = 3
    totient_phi = (prime_p - 1) * (prime_q - 1)
    
    private_d = find_mod_inverse(public_e, totient_phi)
    
    # save strictly to the server folder, away from the student keys
    server_key_path = os.path.join(os.path.dirname(__file__), '..', 'server', 'server_private.pem')
    with open(server_key_path, "w") as server_file:
        server_file.write(f"Election_Server,{private_d},{modulus_n}")
        
    print(f"[*] server private key secured at: {server_key_path}")

# generate keys and insert to db
def generate_student_cohort(total_students=30):
    db_connection = setup_database()
    db_cursor = db_connection.cursor()
    
    # create folder for student pem files
    keys_folder = os.path.join(os.path.dirname(__file__), '..', 'students_keys')
    os.makedirs(keys_folder, exist_ok=True)
    
    prime_list = [i for i in range(100, 500) if is_prime(i)]
    
    print(f"[*] starting key generation for {total_students} students...")
    
    for student_index in range(1, total_students + 1):
        voter_id = f"Student_{student_index:02d}"
        
        # rsa math parameters
        prime_p = random.choice(prime_list)
        prime_q = random.choice(prime_list)
        while prime_q == prime_p:
            prime_q = random.choice(prime_list)

        modulus_n = prime_p * prime_q
        totient_phi = (prime_p - 1) * (prime_q - 1)

        for public_e in [3, 17, 65537]:
            if calculate_gcd(public_e, totient_phi) == 1:
                break
        
        private_d = find_mod_inverse(public_e, totient_phi)

        # write the pem file
        pem_filepath = os.path.join(keys_folder, f"{voter_id}.pem")
        with open(pem_filepath, "w") as key_file:
            key_file.write(f"{voter_id},{private_d},{modulus_n}")
            
        # save public key to sqlite backend
        try:
            db_cursor.execute('''
                INSERT INTO voters (voter_id, public_e, public_n) 
                VALUES (?, ?, ?)
            ''', (voter_id, public_e, modulus_n))
        except sqlite3.IntegrityError:
            print(f"[-] {voter_id} already in database. skipping.")

    db_connection.commit()
    db_connection.close()
    print("[+] setup finished! check students_keys folder")

if __name__ == "__main__":
    generate_server_key() # initialize server first
    generate_student_cohort(30)