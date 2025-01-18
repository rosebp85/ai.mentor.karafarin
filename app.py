from flask import Flask, render_template, request, jsonify
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics.pairwise import cosine_similarity
import os
from sentence_transformers import SentenceTransformer



app = Flask(__name__)  # تعریف اپلیکیشن Flask

# تنظیم برای ارسال کاراکترها به صورت صحیح (غیر از Unicode)
app.config['JSON_AS_ASCII'] = False



file_path = 'data/faq.json'

if not os.path.exists(file_path):
    print(f"Error: File {file_path} not found.")
    faq_data = []  # فایل موجود نیست
else:
    with open(file_path, encoding='utf-8') as f:
        faq_data = json.load(f)  # فایل JSON را به‌عنوان لیست دیکشنری بارگذاری کنید


# حافظه کوتاه‌مدت برای کاربران
user_memory = {}

# مدل NLP و توکنایزر
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def embed_question(question):
    """ایجاد نمایش عددی (embedding) برای سوال"""
    embeddings = model.encode([question])
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
            score = cosine_similarity([question_embedding[0]], [faq_embedding[0]])[0][0]
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
        return jsonify({"response": "لطفاً سوال خود را وارد کنید."})

    response = get_response(user_id, user_message)
    return jsonify({"response": response})







if __name__ == "__main__":
    app.run(debug=True)


