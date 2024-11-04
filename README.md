Configuration for development

1. Install libraries:
pip install requests schedule

2. Generate app password here for SMTP server - https://myaccount.google.com/apppasswords

3. Add system user variables:
SENDER_EMAIL
SENDER_PASSWORD
RECEIVER_EMAILS
CLASS_NAME

============================================

Create docker image
1. docker build -t eeizvertins/school_notifier:v1.0.0 .
2. docker login
3. docker push eeizvertins/school_notifier:v1.0.0

============================================

Create image for both Amd64 and Arm64

Check buildx:
docker buildx create --use
docker buildx inspect --bootstrap

Create image and push to hub:
docker buildx build --platform linux/amd64,linux/arm64 -t eeizvertins/school_notifier:v1.0.0 . --push
