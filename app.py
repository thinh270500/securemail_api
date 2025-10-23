# from flask import Flask, request, jsonify
# from dotenv import load_dotenv
# import os
# import requests
# import html

# load_dotenv()
# app = Flask(__name__)

# SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
# SENDER_EMAIL = os.getenv("SENDER_EMAIL")
# REPLY_TO_EMAIL = os.getenv("REPLY_TO_EMAIL", "phucthinh270500@gmail.com")

# def send_via_sendgrid(to_email, subject, message, sender_name):
#     """Gửi email qua SendGrid HTTP API."""
#     if not SENDER_EMAIL:
#         return {"error": "SENDER_EMAIL must be configured and verified on SendGrid."}, 500

#     url = "https://api.sendgrid.com/v3/mail/send"
#     headers = {
#         "Authorization": f"Bearer {SENDGRID_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     # Validate và escape sender_name để tránh XSS hoặc nội dung không hợp lệ
#     sender_name = html.escape(sender_name) if sender_name and len(sender_name) <= 50 else "Your App Name"

#     # Escape message để tránh lỗi HTML injection
#     message = html.escape(message)

#     # Nội dung email với footer và unsubscribe link
#     plain_text_content = f"Gửi từ: {sender_name}\n\nNội dung:\n{message}\n\n--\nSent by Your Company\nUnsubscribe: https://yourdomain.com/unsubscribe?email={to_email}"
#     html_content = f"""
#     <div style="font-family: Arial, sans-serif; line-height: 1.5;">
#         <h3>Gửi từ: {sender_name}</h3>
#         <p>{message}</p>
#         <hr style="border-top: 1px solid #ccc;">
#         <p style="font-size: 12px; color: #666;">
#             Sent by Your Company Name<br>
#             Address: 123 Your Street, City, Country<br>
#             <a href="https://yourdomain.com/unsubscribe?email={to_email}">Unsubscribe</a> | 
#             <a href="https://yourdomain.com">Visit our website</a>
#         </p>
#     </div>
#     """

#     payload = {
#         "personalizations": [
#             {
#                 "to": [{"email": to_email}],
#                 "subject": subject
#             }
#         ],
#         "from": {
#             "email": SENDER_EMAIL,
#             "name": sender_name
#         },
#         "reply_to": {
#             "email": REPLY_TO_EMAIL,
#             "name": "Leafy"
#         },
#         "content": [
#             {
#                 "type": "text/plain",
#                 "value": plain_text_content
#             },
#             {
#                 "type": "text/html",
#                 "value": html_content
#             }
#         ],
#         "tracking_settings": {
#             "subscription_tracking": {
#                 "enable": True  # Bật unsubscribe link tự động của SendGrid
#             },
#             "click_tracking": {
#                 "enable": True  # Theo dõi click vào link
#             },
#             "open_tracking": {
#                 "enable": True  # Theo dõi mở email
#             }
#         }
#     }

#     r = requests.post(url, headers=headers, json=payload)
#     if r.status_code == 202:
#         return {"id": "Accepted", "status_code": r.status_code}, 200
#     else:
#         return {"error": r.json().get('errors', 'Unknown error'), "status_code": r.status_code}, 500

# @app.route("/send-email", methods=["POST"])
# def send_email():
#     try:
#         if not SENDGRID_API_KEY or not SENDER_EMAIL:
#             return jsonify({"error": "SendGrid API Key or Sender Email is missing in configuration."}), 500
        
#         data = request.get_json()
#         to_email = data.get("to")
#         subject = data.get("subject", "No Subject")
#         message = data.get("message", "")
#         sender_name = data.get("sender", "Your App Name")

#         if not to_email:
#             return jsonify({"error": "Missing 'to' field"}), 400

#         result, status_code = send_via_sendgrid(to_email, subject, message, sender_name)
#         if status_code == 200:
#             return jsonify({"status": "success", "to": to_email, "method": "SendGrid API"}), 200
#         else:
#             return jsonify({"status": "error", "message": result.get('error')}), status_code

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({"message": "Email API is running! (Using SendGrid API)"})

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify
from flask_cors import CORS  # Thêm Flask-CORS
from dotenv import load_dotenv
import os
import requests
import html

load_dotenv()
app = Flask(__name__)

# Cấu hình CORS
# Cách 1: Allow tất cả origin (*)
CORS(app, resources={r"/*": {"origins": "*"}})

# Cách 2 (an toàn hơn): Chỉ định origin cụ thể
# CORS(app, resources={r"/*": {"origins": ["http://localhost:8100", "https://your-ionic-app.com"]}})

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
REPLY_TO_EMAIL = os.getenv("REPLY_TO_EMAIL", "phucthinh270500@gmail.com")

def send_via_sendgrid(to_email, subject, message, sender_name):
    """Gửi email qua SendGrid HTTP API."""
    if not SENDER_EMAIL:
        return {"error": "SENDER_EMAIL must be configured and verified on SendGrid."}, 500

    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    # Validate và escape sender_name để tránh XSS
    sender_name = html.escape(sender_name) if sender_name and len(sender_name) <= 50 else "Encrypted Email Demo"
    message = html.escape(message)  # Escape nội dung mã hóa

    # Nội dung email với footer và unsubscribe link
    plain_text_content = f"""
Gửi từ: {sender_name}

Nội dung mã hóa:
{message}


--
Sent by Encrypted Email Demo
Unsubscribe: https://yourdomain.com/unsubscribe?email={to_email}
"""
    html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.5;">
        <h3>Gửi từ: {sender_name}</h3>
        <p><strong>Nội dung mã hóa:</strong></p>
        <pre>{message}</pre>
        <hr style="border-top: 1px solid #ccc;">
        <p style="font-size: 12px; color: #666;">
            Sent by Encrypted Email Demo<br>
            Address: 123 Your Street, City, Country<br>
            <a href="https://yourdomain.com/unsubscribe?email={to_email}">Unsubscribe</a> | 
            <a href="https://yourdomain.com">Visit our website</a>
        </p>
    </div>
    """

    payload = {
        "personalizations": [
            {
                "to": [{"email": to_email}],
                "subject": subject
            }
        ],
        "from": {
            "email": SENDER_EMAIL,
            "name": sender_name
        },
        "reply_to": {
            "email": REPLY_TO_EMAIL,
            "name": "Encrypted Email Demo"
        },
        "content": [
            {
                "type": "text/plain",
                "value": plain_text_content
            },
            {
                "type": "text/html",
                "value": html_content
            }
        ],
        "tracking_settings": {
            "subscription_tracking": {
                "enable": True
            },
            "click_tracking": {
                "enable": True
            },
            "open_tracking": {
                "enable": True
            }
        }
    }

    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 202:
        return {"id": "Accepted", "status_code": r.status_code}, 200
    else:
        return {"error": r.json().get('errors', 'Unknown error'), "status_code": r.status_code}, 500

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        if not SENDGRID_API_KEY or not SENDER_EMAIL:
            return jsonify({"error": "SendGrid API Key or Sender Email is missing in configuration."}), 500
        
        data = request.get_json()
        to_email = data.get("to")
        subject = data.get("subject", "Encrypted Email Demo")
        message = data.get("message", "")  # Nội dung mã hóa từ Ionic
        sender_name = data.get("sender", "Encrypted Email Demo")

        if not to_email:
            return jsonify({"error": "Missing 'to' field"}), 400

        result, status_code = send_via_sendgrid(to_email, subject, message, sender_name)
        if status_code == 200:
            return jsonify({"status": "success", "to": to_email, "method": "SendGrid API"}), 200
        else:
            return jsonify({"status": "error", "message": result.get('error')}), status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Encrypted Email API is running! (Using SendGrid API)"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)