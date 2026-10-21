
from flask import Flask, render_template, request, redirect, url_for
import qrcode
import sqlite3
import uuid
import os

app = Flask(__name__)

DATABASE = "qrverify.db"
QR_FOLDER = os.path.join("static", "qrcodes")
os.makedirs(QR_FOLDER, exist_ok=True)


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS qr_records (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Valid'
        )
    """)
    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    content = request.form.get("content", "").strip()

    if not content:
        return render_template(
            "index.html",
            message="Please enter some text or a URL.",
            message_type="error"
        )

    record_id = str(uuid.uuid4())
    verification_url = url_for(
        "verify", record_id=record_id, _external=True
    )

    connection = get_db_connection()
    connection.execute(
        "INSERT INTO qr_records (id, content) VALUES (?, ?)",
        (record_id, content)
    )
    connection.commit()
    connection.close()

    qr_image = qrcode.make(verification_url)
    filename = f"{record_id}.png"
    qr_image.save(os.path.join(QR_FOLDER, filename))

    return render_template(
        "index.html",
        message="QR code generated successfully!",
        message_type="success",
        qr_image=filename,
        record_id=record_id,
        content=content
    )


@app.route("/verify/<record_id>")
def verify(record_id):
    connection = get_db_connection()
    record = connection.execute(
        "SELECT * FROM qr_records WHERE id = ?",
        (record_id,)
    ).fetchone()
    connection.close()

    if record is None:
        return render_template(
            "verify.html",
            valid=False,
            message="Invalid QR code: record not found."
        )

    if record["status"] != "Valid":
        return render_template(
            "verify.html",
            valid=False,
            message="This QR code has been revoked."
        )

    return render_template(
        "verify.html",
        valid=True,
        message="QR code verified successfully!",
        record=record
    )


@app.route("/records")
def records():
    connection = get_db_connection()
    all_records = connection.execute(
        "SELECT * FROM qr_records ORDER BY rowid DESC"
    ).fetchall()
    connection.close()

    return render_template("records.html", records=all_records)


@app.route("/revoke/<record_id>", methods=["POST"])
def revoke(record_id):
    connection = get_db_connection()
    connection.execute(
        "UPDATE qr_records SET status = 'Revoked' WHERE id = ?",
        (record_id,)
    )
    connection.commit()
    connection.close()

    return redirect(url_for("records"))


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=False)
