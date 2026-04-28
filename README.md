# Secure E-Voting System

## 1. Project Overview

this project implements a decentralized, zero-knowledge e-voting system built entirely in pyton. designed to meet enginering standards, the system resolves the fundamentals paradox of digital elections: mathematicaly proving the voter's identity to an election commmission while guaranting the absolute secrecy of ballot content.

the system utilizes a client desktop app and a centralized listening server, transmitting strict JSON payloads over a secure conection. it uses asymmetrique encryption.

## 2. Technology Stack

- **Frontend (Client):** `CustomTkinter` — provides a hardware-accelerated, modern desktop GUI. It operates nativelly in Python, allowing direct access to the OS file system for secure RSA Private Key storage and seamless execution of heavy cryptographique math.
    
- **Backend (Election Authority):** Python `socket` — A robust listening server handling concurrent connections, payload validation, and database persistence.
    
- **Data Serialization:** Strict JSON structures for network transmission.

## 4. References & Version Control

The implementation of this secure e-voting architecture relies on a combination of foundational cryptographic literature and modern Python frameworks. Development is managed via strict Git version control to ensure a stable integration.

### Development Tools & Frameworks

- **Python 3.10+:** The core runtime environment.
    
- **[CustomTkinter](https://customtkinter.tomschimansky.com/):** A hardware-accelerated UI framework used to construct the modern, dark-mode desktop client natively in Python.
    
- **Python Standard Library:**
    - `socket` (TCP network transmission)
    
    - `hashlib` (SHA-256 fingerprinting)
        
    - `json` (Payload serialization)
        
    - `sqlite3` (Database persistence)


## 3. Project Setup

### Prerequisites:
- Python 3.10+
- Tk runtime for CustomTkinter
- pip and venv

#### Install Tk (choose your distro):
- Debian/Ubuntu:
    sudo apt update && sudo apt install -y tk8.6 python3-tk
- Fedora:
    sudo dnf install -y tk python3-tkinter
- Arch:
    sudo pacman -S tk

#### Create and activate virtual environment:
    python -m venv .env
    source .env/bin/activate

#### dependencies:
    pip install --upgrade pip
    pip install -r requirements.txt

#### Verify Tk is available:
    python -c "import tkinter; print('Tk OK', tkinter.TkVersion)"

#### Run the client:
    python client.py

### Troubleshooting:
- If you see ImportError: libtk8.6.so: cannot open shared object file:
  - Tk system package is missing, or
  - you are using a different Python interpreter than the one where Tk is available.
- Check interpreter path:
    which python
    python -c "import sys; print(sys.executable)"

### Optional clean start:
    deactivate
    rm -rf .env
    python -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt


### Cryptographic References & Literature

- **The RSA Algorithm:** Rivest, R. L., Shamir, A., & Adleman, L. (1978). _A Method for Obtaining Digital Signatures and Public-Key Cryptosystems_. Communications of the ACM. [Read Paper (PDF)](https://people.csail.mit.edu/rivest/Rsapaper.pdf)
