FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV DISCORD_BOT_TOKEN=""
ENV VERIFICATION_CHANNEL_ID=""
ENV VERIFIED_ROLE_ID=""
ENV SENDER_EMAIL=""
ENV SENDER_EMAIL_PASSWORD=""
ENV EMAIL_DOMAIN=""

CMD ["python", "main.py"]
