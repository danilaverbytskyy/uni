FROM python:3.12-slim

WORKDIR /app
COPY notification_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY notification_service/ .
COPY common ./common

ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
