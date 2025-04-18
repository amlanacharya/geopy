import geocoder
import requests
import time
import schedule
import smtplib
from email.message import EmailMessage

SERVER_URL = "http://127.0.0.1:5000/update_location"


def send_email(lat, lng):
    email = "amlanfgs@gmail.com"
    password = "your_app_password"
    recipient = "rjrocky2580@gmail.com"

    msg = EmailMessage()
    msg.set_content(f"Device location: https://maps.google.com/?q={lat},{lng}")
    msg['Subject'] = "Device Location Update"
    msg['From'] = email
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
            print("Email sent!")
    except Exception as e:
        print(f"Email error: {e}")
def get_location():
    g = geocoder.ip('me')
    return g.latlng if g.ok else None

def send_location():
    location = get_location()
    if location:
        data = {"latitude": location[0], "longitude": location[1]}
        try:
            response = requests.post(SERVER_URL, json=data)
            print("Location sent!" if response.ok else "Failed to send")
        except Exception as e:
            print(f"Error: {e}")

# Update every 5 minutes
schedule.every(5).minutes.do(send_location)

# Initial run
send_location()

while True:
    schedule.run_pending()
    time.sleep(1)