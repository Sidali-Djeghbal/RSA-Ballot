# Secure E-Voting System

## 1. Project Overview

This repository contains a prototype secure e-voting system implemented in Python. It demonstrates a desktop client built with CustomTkinter and a server component that receives and verifies votes. The design focuses on clear, auditable JSON payloads, cryptographic integrity (RSA), and local key handling for the client.

## 2. Technology Stack

- **Client (Desktop):** CustomTkinter (modern Python desktop UI)
- **Server / Network:** Python `socket` (simple TCP listener)
- **Storage & Serialization:** `sqlite3` and JSON


## 3. Project Setup

Prerequisites
- Python 3.10 or newer
- System Tk runtime (required by `tkinter` / CustomTkinter)
- `pip` and `venv` available

Install system Tk (pick your distro):

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install -y tk8.6 python3-tk

# Fedora
sudo dnf install -y tk python3-tkinter

# Arch
sudo pacman -S tk
```

Create and activate a virtual environment, install Python deps:

```bash
python -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Verify Tkinter availability:

```bash
python -c "import tkinter; print('Tk OK', tkinter.TkVersion)"
```

Run the client (from project root):

```bash
python src/client.py
```

Troubleshooting
- If you get "ImportError: libtk8.6.so: cannot open shared object file": install the system Tk package for your distribution and ensure you run the Python interpreter that has access to that Tk installation (the `which python` / `python -c "import sys; print(sys.executable)"` commands help verify the interpreter path).
- If you use multiple Python versions or virtual environments, recreate the venv with the same `python` executable you plan to run.

Optional: clean start

```bash
deactivate || true
rm -rf .env
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## 4. References

- Rivest, R. L., Shamir, A., & Adleman, L. (1978). A Method for Obtaining Digital Signatures and Public-Key Cryptosystems. [PDF](https://people.csail.mit.edu/rivest/Rsapaper.pdf)

