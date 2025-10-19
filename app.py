from flask import Flask, request, jsonify
from dotenv import load_dotenv
import smtplib, os
from email.mime.text import MIMEText

load_dotenv()
app = Flask(__name__)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        to_email = data.get("to")
        subject = data.get("subject", "No Subject")
        message = data.get("message", "")
        sender = data.get("sender", "unknown")

        if not to_email:
            return jsonify({"error": "Missing 'to' field"}), 400

        msg = MIMEText(f"Gửi từ: {sender}\n\nNội dung: {message}")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return jsonify({"status": "success", "to": to_email}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Email API is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
