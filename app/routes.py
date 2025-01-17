from flask import Flask, render_template, request, jsonify
import json
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch

app = Flask(__name__)

# بارگذاری داده‌های سوالات متداول از فایل JSON
with open('data/faq.json', encoding='utf-8') as f:
    faq_data = json.load(f)

# مدل NLP و توکنایزر
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# تابع تولید embedding برای سوال
def embed_question(question):
    inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings

# تابع برای دریافت پاسخ با استفاده از کلیدواژه‌ها و تطابق معنایی
def get_response(user_message):
    question_embedding = embed_question(user_message)
    best_match = None
    best_score = -1

    for item in faq_data:
        # محاسبه شباهت با کلیدواژه‌ها
        if any(keyword in user_message for keyword in item.get("keywords", [])):
            return item["answer"]

        # محاسبه شباهت معنایی
        faq_embedding = embed_question(item["question"])
        score = cosine_similarity(question_embedding.numpy(), faq_embedding.numpy())[0][0]
        if score > best_score:
            best_score = score
            best_match = item

    # بازگرداندن پاسخ مناسب
    if best_match and best_score > 0.7:
        return best_match["answer"]
    else:
        return "متأسفم، نتوانستم پاسخ سوال شما را پیدا کنم."

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get_answer', methods=['POST'])
def get_answer():
    try:
        user_message = request.form.get('message', '').strip()
        if not user_message:
            return jsonify({"error": "لطفاً سوال خود را وارد کنید."}), 400

        response = get_response(user_message)
        return jsonify({"answer": response}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "مشکلی در پردازش درخواست رخ داده است."}), 500
