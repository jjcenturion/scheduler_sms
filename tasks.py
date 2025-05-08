from celeryconfig import app
from send_message import send_sms
from datetime import datetime

@app.task
def send_checkout_sms(phone_number: str, guest_name: str):
    message = f"Hello {guest_name}, check out our late checkout options here: https://checkout.example.com"
    send_sms(phone_number, message)
    print(f"[{datetime.now()}] SMS sent to {phone_number}")
