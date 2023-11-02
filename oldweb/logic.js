function sendMessage() {
    const userMessage = document.getElementById('user-message').value;

    if (userMessage.trim() === '') {
        return;
    }
    appendMessage('You', 'userstyle', userMessage);
    callCharServerAndStoreResponse(userMessage);
}

function appendMessage(sender, styleClass, message) {
    const chatLog = document.getElementById('chat-log');
    const messageElement = document.createElement('div');

    messageElement.classList.add(styleClass);
    messageElement.innerHTML = sender + ': ' + message;
    chatLog.appendChild(messageElement);
}

const URL = 'http://10.10.240.11:5005/api/';

function callCharServerAndStoreResponse(userMessage) {
    fetch(URL + 'chat?question=' + userMessage)
    .then(response => {
        if (response.ok) {
            return response.text();
        }
    })
    .then(function(data) {
        console.log(data);

        appendMessage('Charlie',  'botstyle', data);
        const log = document.getElementById("chat-log");
        log.scrollTop = log.scrollHeight;
        document.getElementById('user-message').value = '';
    })
    .catch(function(error) {
        console.error(error);
        alert('Error: server not available - did you forget "python server.py" on server machine?')
    });
}
