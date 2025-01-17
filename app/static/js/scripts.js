document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("question-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // جلوگیری از رفرش صفحه

        const questionInput = document.getElementById("message");
        const question = questionInput.value.trim();

        if (!question) {
            alert("لطفاً سوال خود را وارد کنید.");
            return;
        }

        // ارسال درخواست به سرور
        fetch("/get_answer", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                user_id: "12345", // آی‌دی کاربر (می‌توانید تنظیم کنید)
                message: question,
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("خطا در پاسخ سرور");
                }
                return response.json();
            })
            .then((data) => {
                // نمایش پاسخ
                if (data.answer) {
                    const answerContainer = document.getElementById("answer-container");
                    const botAnswer = document.getElementById("bot-answer");

                    botAnswer.textContent = data.answer;
                    answerContainer.style.display = "block";
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("مشکلی در ارسال درخواست رخ داده است.");
            });
    });
});
