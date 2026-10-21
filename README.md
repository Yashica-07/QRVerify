# QRVerify — QR Code Generation and Verification System

QRVerify is a web application built with Flask that generates unique QR codes and allows users to verify records by scanning them. It supports record management and revocation, with status information displayed on a simple, cybersecurity-inspired interface.

## Features

- Generate unique QR codes for records.
- Verify records using a unique verification URL.
- View all generated records and their statuses.
- Revoke records and mark them as invalid.
- Store record information using SQLite.
- Responsive web interface built with HTML, CSS, and JavaScript.

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **QR Code Generation:** Python `qrcode` and Pillow
- **Version Control:** Git and GitHub

## Project Structure

```text
QRVerify/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── index.html
│   ├── records.html
│   └── verify.html
└── static/
    └── qrcodes/
```

The SQLite database, generated QR images, and Python virtual environment are kept locally and excluded from Git.

## Prerequisites

- Python installed
- Git installed
- PowerShell or another terminal

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/Yashica-07/QRVerify.git
   cd QRVerify
   ```

2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000` in your browser.

## How It Works

1. Enter record information into the application.
2. Generate a QR code linked to the record's verification page.
3. Scan the QR code to view the record's current status.
4. View records and revoke a record when required.
5. Verify the record again to see its updated status.

**Note:** QRVerify reports the status stored in its database. A valid status indicates that the record exists and has not been revoked; it does not independently guarantee the truthfulness of the underlying information.

## DevOps Learning Objectives

This project is being developed as a DevOps case study covering:

- Git and GitHub source code management
- Jenkins continuous integration and delivery
- Docker containerization
- Kubernetes deployment and management
- Selenium-based browser testing

## Author

**Gaddam Yashica**

GitHub: https://github.com/Yashica-07
