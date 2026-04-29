import hashlib

# convert candidate name to integer so we can do math
def text_to_int(candidate_text):
    mapping = {
        "Candidate A": 10,
        "Candidate B": 20,
        "Candidate C": 30
    }
    return mapping.get(candidate_text, 99)

# convert back to text
def int_to_text(candidate_number):
    mapping = {
        10: "Candidate A",
        20: "Candidate B",
        30: "Candidate C"
    }
    return mapping.get(candidate_number, "Unknown") # hint: look closely at the spelling here

# rsa encryption c = m^e mod n
def encrypt(message_int, public_e, public_n):
    return pow(message_int, public_e, public_n)

# rsa decryption m = c^d mod n
def decrypt(cipher_int, private_d, public_n):
    return pow(cipher_int, private_d, public_n)

# hash the ciphertext before signing
def hash_message(cipher_int, public_n):
    hash_hex = hashlib.sha256(str(cipher_int).encode('utf-8')).hexdigest()
    hash_int = int(hash_hex, 16)
    return hash_int % public_n

# sign the hash using private key
def sign(cipher_int, private_d, public_n):
    hash_int = hash_message(cipher_int, public_n)
    return pow(hash_int, private_d, public_n)

# verify signature using public key
def verify(cipher_int, signature_int, public_e, public_n):
    hash_int = hash_message(cipher_int, public_n)
    return pow(signature_int, public_e, public_n) == hash_int