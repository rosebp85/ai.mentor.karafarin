document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("question-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // جلوگیری از ارسال فرم به روش سنتی

        const questionInput = document.getElementById("message");
        const question = questionInput.value.trim();

        if (!question) {
            alert("لطفاً سوال خود را وارد کنید.");
            return;
        }

        // ارسال درخواست به سرور
        fetch("/get_answer", {
            method: "POST", // اطمینان از ارسال متد POST
            headers: {
                "Content-Type": "application/x-www-form-urlencoded", // نوع محتوای درخواست
            },
            body: new URLSearchParams({
                message: question, // ارسال پارامتر پیام
            }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("خطا در پاسخ سرور");
                }
                return response.json();
            })
            .then((data) => {
                if (data.answer) {
                    document.getElementById("bot-answer").textContent = data.answer;
                    document.getElementById("answer-container").style.display = "block";
                }
            })
            .catch((error) => {
                console.error("Error:", error); // چاپ خطا
                alert("مشکلی در ارسال درخواست رخ داده است.");
            });
    });
});
