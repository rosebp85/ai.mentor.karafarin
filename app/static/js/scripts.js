document.getElementById("question-form").addEventListener("submit", function (event) {
    event.preventDefault(); // جلوگیری از ارسال فرم به روش سنتی

    const question = document.getElementById("message").value.trim();
    if (!question) {
        alert("لطفاً سوال خود را وارد کنید.");
        return;
    }

    fetch("/get_answer", {
        method: "POST", // ارسال درخواست با متد POST
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            user_id: "12345",
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
            if (data.answer) {
                document.getElementById("bot-answer").textContent = data.answer;
                document.getElementById("answer-container").style.display = "block";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("خطا در ارسال درخواست.");
        });
});
