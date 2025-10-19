# from flask import Flask, request, jsonify
# from dotenv import load_dotenv
# import smtplib, os
# from email.mime.text import MIMEText

# load_dotenv()
# app = Flask(__name__)

# EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# @app.route("/send-email", methods=["POST"])
# def send_email():
#     try:
#         data = request.get_json()
#         to_email = data.get("to")
#         subject = data.get("subject", "No Subject")
#         message = data.get("message", "")
#         sender = data.get("sender", "unknown")

#         if not to_email:
#             return jsonify({"error": "Missing 'to' field"}), 400

#         msg = MIMEText(f"Gửi từ: {sender}\n\nNội dung: {message}")
#         msg["From"] = EMAIL_ADDRESS
#         msg["To"] = to_email
#         msg["Subject"] = subject

#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#             smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#             smtp.send_message(msg)

#         return jsonify({"status": "success", "to": to_email}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({"message": "Email API is running!"})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests  # Import thư viện requests

load_dotenv()
app = Flask(__name__)

# Lấy Resend API Key từ biến môi trường
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# --- HÀM GỬI EMAIL MỚI DÙNG RESEND API ---
def send_via_resend(to_email, subject, message, sender):
    """Gửi email qua Resend HTTP API."""
    url = "https://api.resend.com/emails"
    headers = {
        # Dùng RESEND_API_KEY để xác thực
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Địa chỉ gửi đi, sử dụng domain miễn phí của Resend trong ví dụ
    # Nếu anh đã xác minh domain của mình, hãy thay đổi @resend.dev bằng domain của anh.
    from_email = f"SecureMail <{sender}@resend.dev>"
    
    payload = {
        "from": from_email,
        "to": [to_email], # Resend chấp nhận danh sách
        "subject": subject,
        # Nên dùng "html" thay vì "text" để dễ định dạng
        "html": f"<h3>Gửi từ: {sender}</h3><p>Nội dung:</p><p>{message}</p>"
    }
    
    r = requests.post(url, headers=headers, json=payload)
    
    # Trả về kết quả JSON từ Resend
    return r.json()

# --- ROUTES ---

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        if not RESEND_API_KEY:
            return jsonify({"error": "RESEND_API_KEY is not configured"}), 500
        
        data = request.get_json()
        to_email = data.get("to")
        subject = data.get("subject", "No Subject")
        message = data.get("message", "")
        sender = data.get("sender", "unknown")

        if not to_email:
            return jsonify({"error": "Missing 'to' field"}), 400

        # GỌI HÀM GỬI EMAIL BẰNG RESEND
        result = send_via_resend(to_email, subject, message, sender)
        
        # Kiểm tra phản hồi của Resend để xác định thành công
        if 'id' in result:
            return jsonify({"status": "success", "to": to_email, "resend_id": result['id']}), 200
        else:
            # Resend trả về lỗi nếu không có 'id'
            return jsonify({"status": "error", "message": result.get('message', 'Resend API error')}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Email API is running! (Using Resend)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)