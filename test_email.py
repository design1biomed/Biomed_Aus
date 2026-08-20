import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

user = os.environ.get('EMAIL_HOST_USER')
password = os.environ.get('EMAIL_HOST_PASSWORD')

print(f"Testing SMTP for {user}")

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password)
    print("SUCCESS: Logged in successfully!")
    server.quit()
except Exception as e:
    print("ERROR:")
    print(str(e))
