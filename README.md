# Secure E-Voting System

## 1. Project Overview

this project implements a decentralized, zero-knowledge e-voting system built entirely in pyton. designed to meet advanced enginering standards, the system resolves the fundamentals paradox of digital elections: mathematicaly proving the voter's identity to an election commmission while guaranting the absolute secrecy of ballot content.

the system utilizes a client desktop app and a centralized listening server, transmitting strict JSON payloads over a secure conection. it uses asymmetrique encryption.

## 2. Technology Stack

- **Frontend (Client):** `CustomTkinter` — provides a hardware-accelerated, modern desktop GUI. It operates nativelly in Python, allowing direct access to the OS file system for secure RSA Private Key storage and seamless execution of heavy cryptographique math without browser sandbox limits.
    
- **Backend (Election Authority):** Python `socket` / `FastAPI` — A robust listening server handling concurrent connections, payload validation, and database persistence.
    
- **Data Serialization:** Strict JSON structures for network transmission.

## 3. system componennts 

### repo structure

```
RSA-Ballot/
├── frontend/
│   ├── app.py                 # CustomTkinter UI rendering
│   ├── crypto_engine.py       # local RSA KeyGen, DHE logic..
│   └── keys/                  # local directory for the Private Key
├── backend/
│   ├── server.py              # socket listener / API router
│   ├── verification.py        # signature validation and DHE parameter generation
│   └── database/              # SQLite DB for registered_keys and stored_commitments
```

## 4. References & Version Control

The implementation of this secure e-voting architecture relies on a combination of foundational cryptographic literature and modern Python frameworks. Development is managed via strict Git version control to ensure a stable integration.

### Source Code & Workflow

- **Project Repository:** [RSA-Ballot (GitHub)](https://github.com/Sidali-Djeghbal/RSA-Ballot/)
        
- **Task Management:** A GitHub Project board will be established to track feature implementation, monitor cryptographic milestones, and ensure delivery before the April 30, 2026 deadline.
    

### Development Tools & Frameworks

- **Python 3.10+:** The core runtime environment.
    
- **[CustomTkinter](https://customtkinter.tomschimansky.com/):** A hardware-accelerated UI framework used to construct the modern, dark-mode desktop client natively in Python.
    
- **[Cryptography.io](https://cryptography.io/en/latest/):** The Python standard for robust, production-grade cryptographic primitives (utilized specifically for the Diffie-Hellman exchange and AES-256 Fernet encryption).
    
- **Python Standard Library:** * `socket` (TCP network transmission)
    
    - `hashlib` (SHA-256 fingerprinting)
        
    - `json` (Payload serialization)
        
    - `sqlite3` (Database persistence)

### Cryptographic References & Literature

- **The RSA Algorithm:** Rivest, R. L., Shamir, A., & Adleman, L. (1978). _A Method for Obtaining Digital Signatures and Public-Key Cryptosystems_. Communications of the ACM. [Read Paper (PDF)](https://people.csail.mit.edu/rivest/Rsapaper.pdf)

- **Pedersen Commitment Schemes:** Pedersen, T. P. (1991). _Non-Interactive and Information-Theoretic Secure Verifiable Secret Sharing_. Advances in Cryptology — CRYPTO '91. This paper provides the mathematical foundation for the "Absolute Secrecy" locked-box mechanism. [Springer Link](https://link.springer.com/chapter/10.1007/3-540-46766-1_9)
    
- **Perfect Forward Secrecy (PFS):** An overview of the Diffie-Hellman Ephemeral (DHE) key exchange and its critical role in preventing retrospective decryption of intercepted network traffic. [RFC 2631 - Diffie-Hellman Key Agreement Method](https://datatracker.ietf.org/doc/html/rfc2631)
