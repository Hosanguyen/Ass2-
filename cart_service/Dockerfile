# Sử dụng Python image
FROM python:3.10

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file yêu cầu vào container
COPY requirements.txt .

# Cài đặt thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 8000 (mặc định của Django)
EXPOSE 1111

# Lệnh chạy server Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:1111"]
