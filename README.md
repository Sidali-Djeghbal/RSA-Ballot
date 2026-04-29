
# Secure E-Voting System (Client-Server)

This project was built as an educational demonstration of modern cryptography principles, implementing RSA math from scratch without relying on high-level encryption wrappers.

## Cryptographic Guarantees

This system ensures five core pillars of secure elections:

| Security Challenge | Technical Solution | Practical Result |
| :--- | :--- | :--- |
| **Confidentiality** | Server's Public Key Encryption | The message is unreadable during transit; no one on the network can see the vote. |
| **Authenticity** | Client's Private Key Signature | The server mathematically verifies that the vote originated from a specific registered voter. |
| **Integrity** | SHA-256 Hashing | A network interceptor cannot flip bits to change a vote from "Candidate A" to "Candidate C". |
| **Uniqueness** | SQLite State Management | Double-voting is strictly prevented; voters are marked after participating. |
| **Relative Anonymity**| Segregated Server Logic | The server verifies the signature (the *who*) separately from tallying the vote (the *what*). |

## Project Structure

```text
RSA_Ballot/
├── common/                     # Shared logic needed by both client and server
│   └── rsa_core.py             # Custom RSA mathematical engine and hashing logic
├── server/                     # The Central Authority (Digital Ballot Box)
│   ├── server.py               # Socket listener and SQLite logic
│   └── election.db             # Auto-generated SQLite database (IGNORED IN GIT)
├── client/                     # The Voter Interface
│   ├── client.py               # Modern CustomTkinter GUI
│   └── assets/                 # UI resources (e.g., avatar images)
├── scripts/                    # Admin/Initialization Utilities
│   └── setup_election.py       # Generates cohort keys, server keys, and initializes DB
├── students_keys/              # Auto-generated directory containing Voter .pem files (IGNORED IN GIT)
├── requirements.txt            # UI dependencies
├── .gitignore                  # Version control exclusions for security
└── README.md                   # Project documentation
```

## Getting Started

### Prerequisites & Installation
Ensure you have Python 3.x installed. It is highly recommended to use a virtual environment to manage the GUI dependencies cleanly.

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install the required GUI libraries
pip install -r requirements.txt
```

### Step 1: Initialize the Election
Before anyone can vote, the election administrator must generate the cryptographic keys for the server and the registered voters, and set up the SQLite database.

```bash
python3 scripts/setup_election.py
```
* **What this does:** 
1. Generates `server/server_private.pem` (The Server's Private Key).
2. Generates 30 `.pem` files in `students_keys/` (The Voters' Private Keys).
3. Initializes `server/election.db` with the public keys of all voters.

### Step 2: Start the Digital Ballot Box (Server)
Open a terminal and start the server so it can listen for incoming secure votes.

```bash
python3 server/server.py
```
* **Note:** Leave this terminal running in the background. It will silently log identity verifications without leaking the actual votes.

### Step 3: Launch the Voter Interface (Client)
Open a **new terminal window**, activate your virtual environment again, and launch the UI:

```bash
source .venv/bin/activate
python3 client/client.py
```

### How to Vote
1. On the client GUI, click **"load identity (.pem)"**.
2. Navigate to the `students_keys/` folder and select one of the `Student_XX.pem` files.
3. Select your preferred candidate and click **"submit secure vote"**.
4. Check the Server terminal to see the cryptography in action! Try voting again with the exact same `.pem` file to test the anti-double-vote system.

## Educational Limitations
This project contains intentional educational simplifications:
* **Small Prime Numbers:** The RSA key generator uses small prime numbers (100–500) to keep the mathematics traceable and human-readable during demonstrations.
* **No Padding:** Standard RSA padding (like OAEP) is omitted to simplify the core `rsa_core.py` engine.
* **Out-of-Band Key Distribution:** In a real-world scenario, the `.pem` files generated in the `students_keys/` folder would be physically distributed to voters on secure USB drives after verifying physical identification.
