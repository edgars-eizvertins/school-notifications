import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
import schedule
import time
import os
from datetime import datetime, timedelta

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAILS = os.getenv("RECEIVER_EMAILS").split(",")
CLASS_NAME = os.getenv("CLASS_NAME")
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME")

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
		log(f"Error checking image: {e}")
		return False

def send_email(image_url):
	try:
		log("Sending email...")		
		msg = MIMEMultipart()
		msg['From'] = formataddr(('72 school notification', SENDER_EMAIL))
		msg['To'] = ', '.join(RECEIVER_EMAILS)
		msg['Subject'] = f'There are changes in schedule for {CLASS_NAME}'
		body = 'You can see changes in schedule here: ' + image_url.replace(' ', '%20')
		img_response = requests.get(image_url)
		img_response.raise_for_status()
		image = MIMEImage(img_response.content, name=os.path.basename(image_url))
		msg.attach(image)
		msg.attach(MIMEText(body))
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
			server.login(SENDER_EMAIL, SENDER_PASSWORD)
			server.send_message(msg)
			log("Email sent successfully!")
	except Exception as e:
		log(f"Error sending email: {e}")

def job():
	if is_workday_tomorrow():
		image_url = get_next_workday_image_url()
		log(image_url);
		if check_image_exists(image_url):
			send_email(image_url)
		else:
			log(f"No changes in schedule for {CLASS_NAME}")
			log("Image does not exist. No image sent.")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

log("Starting...")
log(f"SENDER_EMAIL: {SENDER_EMAIL}")
log(f"RECEIVER_EMAILS: {RECEIVER_EMAILS}")
log(f"CLASS_NAME: {CLASS_NAME}")
log(f"SCHEDULE_TIME: {SCHEDULE_TIME}")

schedule.every().day.at(SCHEDULE_TIME).do(job)
# wait while containers starts and then start running
log("Initializing...")
time.sleep(60)
log("Working...")
job()

while True:
	schedule.run_pending()    
	time.sleep(30)
