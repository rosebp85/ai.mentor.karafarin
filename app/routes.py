from app import app
from flask import render_template, request, jsonify
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics.pairwise import cosine_similarity



# بارگذاری داده‌های سوالات متداول از فایل JSON
with open('data/faq.json', encoding='utf-8') as f:
    faq_data = json.load(f)

# حافظه کوتاه‌مدت برای کاربران
user_memory = {}

# مدل NLP و توکنایزر
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def embed_question(question):
    """ایجاد نمایش عددی (embedding) برای سوال"""
    inputs = tokenizer(question, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.logits.numpy()
    return embeddings

def get_response(user_id, user_message):
    """مدیریت مکالمه کاربر و ارائه پاسخ مناسب"""
    if user_id not in user_memory:
        user_memory[user_id] = {"state": "waiting_for_question", "history": []}

    state = user_memory[user_id]["state"]
    user_memory[user_id]["history"].append({"user": user_message})

    if state == "waiting_for_question":
        question_embedding = embed_question(user_message)
        best_match = None
        best_score = -1

        for item in faq_data:
            faq_embedding = embed_question(item["question"])
            score = cosine_similarity(question_embedding, faq_embedding)[0][0]
            if score > best_score:
                best_score = score
                best_match = item

        if best_match and best_score > 0.7:
            response = best_match["answer"]
        else:
            response = "متاسفم، نتوانستم پاسخ سوال شما را پیدا کنم."

        user_memory[user_id]["state"] = "waiting_for_question"
    else:
        response = "متاسفم، متوجه درخواست شما نشدم."
        user_memory[user_id]["state"] = "waiting_for_question"

    user_memory[user_id]["history"].append({"bot": response})
    return response





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_id = request.form.get('user_id', 'unknown_user')
    user_message = request.form.get('message', '')

    if not user_message:
        return "لطفاً سوال خود را وارد کنید."  # بازگرداندن متن ساده

    response = get_response(user_id, user_message)
    print(f"Response: {response}")  # چاپ پاسخ در کنسول برای بررسی
    return response  # بازگرداندن پاسخ به‌صورت مستقیم
