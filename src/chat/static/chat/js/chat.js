const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=')
            if (key === name) {
                return decodeURIComponent(value)
            }
        }
    }
}
const csrftoken = getCookie('csrftoken')

const sendMessage = document.getElementById('chat-form')
sendMessage.addEventListener('submit', (event) => {
    event.preventDefault();
    const url = '{% url "session_detail" session.id %}'

    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (message !== '') {
        // フォームの中のbutton要素を取得して、aria-busy属性をtrueに設定
        const button = document.getElementById('chat-button');
        button.setAttribute('aria-busy', 'true');
        
        const body = new URLSearchParams();
        body.append('content', message);
        console.log(body);


        fetch(url, {
            method: 'POST',
            body: body,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-CSRFToken': csrftoken,
            }
        })
            .then(response => {
                return response.json();
            })
            .then((response) => {
                if (response.success) {
                    const chatBox = document.getElementById('chat-box');

                    // User message
                    const userMessage = document.createElement('div');
                    userMessage.classList.add('message', 'user');
                    userMessage.innerHTML = `<span><strong>${response.username}</strong>: ${response.content} <em>(${response.created_at})</em></span>`;
                    chatBox.appendChild(userMessage);

                    // AI response
                    const aiMessage = document.createElement('div');
                    aiMessage.classList.add('message', 'ai');
                    aiMessage.innerHTML = `<span><strong>${response.ai_response.username}</strong>: ${response.ai_response.content} <em>(${response.ai_response.created_at})</em></span>`;
                    chatBox.appendChild(aiMessage);

                    input.value = '';
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            })
            .catch(error => console.error('Error:', error));
    }
})