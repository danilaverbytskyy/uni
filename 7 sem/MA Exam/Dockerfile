FROM python:3.13-slim

WORKDIR /flask-app

RUN pip install flask

COPY flask-app.py .

EXPOSE 5000

CMD ["python", "flask-app.py"]
