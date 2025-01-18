document.getElementById("question-form").addEventListener("submit", function (event) {
    event.preventDefault(); // جلوگیری از ارسال فرم به روش سنتی

    const question = document.getElementById("message").value.trim();
    if (!question) {
        alert("لطفاً سوال خود را وارد کنید.");
        return;
    }

    // مخفی کردن کادر پاسخ قبلی
    const answerContainer = document.getElementById("answer-container");
    answerContainer.style.display = "none";  // کادر پاسخ را مخفی می‌کنیم

    // ارسال سوال به سرور
    fetch("/get_answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            user_id: "12345",
            message: question
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("خطا در دریافت پاسخ از سرور.");
            }
            return response.json(); // انتظار دریافت JSON
        })
        .then(data => {
            if (data && data.response) {
                // نمایش پاسخ در کادر
                document.getElementById("bot-answer").textContent = data.response;
                answerContainer.style.display = "block"; // نمایش کادر پاسخ
            } else {
                alert("پاسخی دریافت نشد.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("خطا در ارسال درخواست.");
        });
});
