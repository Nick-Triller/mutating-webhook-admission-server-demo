FROM python:3.8-alpine

WORKDIR /app

# Setup the app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# Run the app
CMD flask run --host=0.0.0.0 --cert "$WEBHOOK_SERVER_CERT_CRT" --key "$WEBHOOK_SERVER_CERT_KEY"
