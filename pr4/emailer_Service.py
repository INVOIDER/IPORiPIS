from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from waitress import serve

app = Flask(__name__)



def send_email(from_email,smtp_server,smtp_port,to_address, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_address

    with smtplib.SMTP(smtp_server,smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.set_debuglevel(1)

        server.login(from_email, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route("/", methods=['POST'])
def index():
    if request.method == 'POST':
        from_email = request.form.get('from')
        from_email_password = request.form.get('password')
        smtp_server = request.form.get('smtp_server')
        smtp_port = request.form.get('smtp_port')
        to_email = request.form.get('to')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not to_email or not subject or not message:
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            send_email(from_email,smtp_server,smtp_port,to_email, subject, message)
            return jsonify({'status': 'Email sent successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return '''
        <form method="post">
            To: <input name="to"><br>
            Subject: <input name="subject"><br>
            Message: <textarea name="message"></textarea><br>
            <input type="submit" value="Send">
        </form>
    '''

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=1516)
