from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')

def subscription_email(id):
    to = id.decode('utf-8')
    print(f"Subscription email would be sent to: {to}")
    print("Email content: Thank you! Your Subscription to club has been confirmed")

def registration_email(id):
    to = id.decode('utf-8')
    print(f"Registration email would be sent to: {to}")
    print("Email content: Thank you! Your registration for the event has been confirmed")

def send_email(message):
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(e.message)