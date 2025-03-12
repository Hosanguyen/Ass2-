FROM python:3.10

WORKDIR /payment_service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 6800

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:6800"]