import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import schedule
import time
import os
import time
from datetime import datetime, timedelta
from urllib.parse import quote

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAILS = ["edgars.eizvertins@gmail.com"]

CLASS_NAME = "1.a"
BASE_IMAGE_URL = "https://72skola.lv/saraksts/{}/{}.Png"

MONTHS = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

def is_workday_tomorrow():
	today = datetime.now()
	tomorrow = today + timedelta(days=1)

	if tomorrow.weekday() < 5:  # 0-4 are Monday-Friday
		return True
	return False

def get_next_workday_image_url():
	today = datetime.now()
	next_workday = today + timedelta(days=1)
	if next_workday.weekday() == 5:  # Saturday
		next_workday += timedelta(days=2)  # Move to Monday
	elif next_workday.weekday() == 6:  # Sunday
		next_workday += timedelta(days=1)  # Move to Monday

	# Format the date to "Nov 4.Png"
	image_date = f"{MONTHS[next_workday.month]} {next_workday.day}"
	return BASE_IMAGE_URL.format(CLASS_NAME, image_date)

def check_image_exists(url):
	try:
		response = requests.head(url)
		return response.status_code == 200
	except Exception as e:
		print(f"Error checking image: {e}")
		return False

def send_email(image_url):
	try:
		msg = MIMEMultipart()		
		msg['From'] = formataddr(('Your Name', SENDER_EMAIL))
		msg['To'] = ', '.join(RECEIVER_EMAILS)
	
		if (image_url is None):
			subject = f'No changes in schedule for {CLASS_NAME}'
			body = "No changes in schedule"
		else:
			subject = f'There are changes in schedule for {CLASS_NAME}'
			body = 'You can see changes in schedule here: ' + image_url.replace(' ', '%20')
			img_response = requests.get(image_url)
			img_response.raise_for_status()
			image = MIMEImage(img_response.content, name=os.path.basename(image_url))
			msg.attach(image)

		msg['Subject'] = subject
		msg.attach(MIMEText(body))

		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
			server.login(SENDER_EMAIL, SENDER_PASSWORD)
			server.send_message(msg)
			print("Email sent successfully!")
	except Exception as e:
		print(f"Error sending email: {e}")

def job():
	if is_workday_tomorrow():
		image_url = get_next_workday_image_url()
		print(image_url);
		if check_image_exists(image_url):
			send_email(image_url)
		else:
			send_email(None)
			print("Image does not exist. No image sent.")

schedule.every().day.at("20:00").do(job)

while True:
	# schedule.run_pending()
	job()    
	time.sleep(30)
