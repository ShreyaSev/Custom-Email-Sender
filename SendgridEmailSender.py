import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, SendAt , PlainTextContent, HtmlContent
import markdown

from pymongo import MongoClient
from datetime import datetime




from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY2")
FROM_EMAIL = "shreyasevelar1@gmail.com"
TO_EMAIL = "shreyasevelar1@gmail.com"

class EmailSender:

    def __init__(self):
        # MongoDB connection URI
        self.client = MongoClient('mongodb://localhost:27017/')  # for local MongoDB
        self.db = self.client['email_tracking']  # Database name
        self.emails_collection = self.db['emails_sent']  # Collection name

    def send_email(self, to_email, message_content, personalisations_dict = None):
        # html_content=f'<script type="module" src="https://md-block.verou.me/md-block.js"></script>\
        # <md-block>\
        # <p>If you cannot see this email, please check your email settings or view it online.</p>\
        #                 <p>{message_content}</p> </md-block>'
        html_content = markdown.markdown(message_content) 
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails= to_email,
            subject='Sending with Twilio SendGrid is Fun',
            )
        message.add_content(HtmlContent(html_content))
        message.add_content(PlainTextContent(message_content))
        
        send_at = personalisations_dict["send_at"]
        message.send_at = SendAt(send_at)
        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

if __name__=="__main__":
    es = EmailSender()
    es.send_email(TO_EMAIL, "Hello, this is a test email", {"send_at" : None})
