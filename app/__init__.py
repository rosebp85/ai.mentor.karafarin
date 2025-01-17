from flask import Flask

# ساخت اپلیکیشن Flask
app = Flask(__name__)

# وارد کردن مسیرها
from app import routes
