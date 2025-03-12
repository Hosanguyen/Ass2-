# Sử dụng image Python mới nhất
FROM python:3.11

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Chạy lệnh migrate database
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8100"]
