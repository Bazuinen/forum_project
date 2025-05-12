
function toggleChat() {
    const chatSection = document.getElementById('chat-section');
    chatSection.classList.toggle('active');
}
document.getElementById('chat-message').focus();

setTimeout(() => {
    chatBox.scrollTop = chatBox.scrollHeight;
    document.getElementById('chat-message').focus();
}, 100);
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function loadChatMessages() {
    fetch("/get-chat-messages/")
        .then(response => response.json())
        .then(data => {
            const chatBox = document.getElementById("chat-box");
            chatBox.innerHTML = '';  // Leeg de chatbox

            data.messages.reverse().forEach(msg => {
                const p = document.createElement("p");
                p.innerHTML = `<strong>${msg.user}:</strong> ${msg.message}`;
                chatBox.appendChild(p);
            });

            chatBox.scrollTop = chatBox.scrollHeight;
        });
}

document.addEventListener("DOMContentLoaded", function () {
    loadChatMessages();
});


const csrftoken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const input = document.getElementById("chat-message");
    const chatBox = document.getElementById("chat-box");

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        fetch("/send-chat-message/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: `message=${encodeURIComponent(input.value)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                const p = document.createElement("p");
                p.innerHTML = `<strong>${data.user}:</strong> ${data.message}`;
                chatBox.appendChild(p);
                chatBox.scrollTop = chatBox.scrollHeight;
                input.value = "";
                loadChatMessages();
            }
        });
    });

    // CSRF helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
