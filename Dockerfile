# انتخاب پایتون به عنوان بیس ایمیج
FROM python:3.10

# تغییر دایرکتوری کاری به دایرکتوری پروژه
WORKDIR /app

# کپی کردن فایل requirements.txt به دایرکتوری پروژه
COPY requirements.txt .

# ایجاد محیط مجازی
RUN python -m venv venv

# فعال کردن محیط مجازی و نصب پکیج‌ها
RUN ./venv/bin/pip install -r requirements.txt

# کپی کردن بقیه فایل‌ها
COPY . .

# فعال کردن محیط مجازی و اجرای برنامه
CMD ["./venv/bin/python", "main.py"]
