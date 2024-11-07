import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, SendAt

from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "sevelarshreya@gmail.com"
TO_EMAIL = "sevelarshreya@gmail.com"


def send_email(to_email, message_content, personalisations_dict):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails= TO_EMAIL,
        subject='Sending with Twilio SendGrid is Fun',
        # html_content=f'<{message_content}</strong>')
        plain_text_content=message_content)
    send_at = personalisations_dict["send_at"]
    message.send_at = SendAt(send_at)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)