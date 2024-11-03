import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import os
import time
from datetime import datetime, timedelta

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAILS = ["edgars.eizvertins@gmail.com"]

# URL to check
URL = "https://72skola.lv/saraksts/index.htm"

def check_for_class_updates():
	try:
		print(f"Senders email {SENDER_EMAIL}")
		
		print(f"Checking school page...")
		response = requests.get(URL)
		response.raise_for_status()

		print(f"Parsing HTML...")
		soup = BeautifulSoup(response.text, 'html.parser')
		if "1.d" in soup.text:
			send_email_notification()
	except requests.RequestException as e:
		print(f"Error fetching the page: {e}")

def send_email_notification():
	for recipient in RECEIVER_EMAILS:
		# Prepare email
		msg = MIMEMultipart()
		msg["From"] = SENDER_EMAIL
		msg["To"] = recipient
		msg["Subject"] = "School Schedule Update for Class 1.d"

		body = "There are updates in the schedule for class 1.d. Please check the school site for more details."
		msg.attach(MIMEText(body, "plain"))

		try:
			with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
				server.starttls()
				server.login(SENDER_EMAIL, SENDER_PASSWORD)
				server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
			print(f"Email sent to {recipient}")
		except Exception as e:
			print(f"Error sending email: {e}")

def is_workday_tomorrow():
	today = datetime.now()
	tomorrow = today + timedelta(days=1)

	if tomorrow.weekday() < 5:  # 0-4 are Monday-Friday
		return True
	return False

def job():
	if is_workday_tomorrow():
		check_for_class_updates()

schedule.every().day.at("20:00").do(job)

while True:
	schedule.run_pending()
	check_for_class_updates()    
	time.sleep(30)
