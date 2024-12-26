// // Function to send a message
// document.getElementById('sendBtn').addEventListener('click', () => {
//     const messageInput = document.getElementById('messageInput');
//     const messageText = messageInput.value;

//     if (messageText) {
//         appendMessage(messageText, 'outgoing');
//         messageInput.value = ''; // Clear input after sending
//     }
// });

// // Function to append message to chat area
// function appendMessage(text, type) {
//     const chatArea = document.getElementById('chatArea');
//     const messageDiv = document.createElement('div');
//     messageDiv.classList.add('message', type);
    
//     const messageContent = `
//         <div class="message-content">
//             <p>${text}</p>
//             <span class="timestamp">${new Date().toLocaleTimeString()}</span>
//         </div>`;
    
//     messageDiv.innerHTML = messageContent;
//     chatArea.appendChild(messageDiv);
//     chatArea.scrollTop = chatArea.scrollHeight; // Auto-scroll to bottom
// }

// // File Attachment Button
// document.getElementById('attachBtn').addEventListener('click', () => {
//     document.getElementById('fileInput').click(); // Trigger file input
// });

// document.getElementById('fileInput').addEventListener('change', (event) => {
//     const file = event.target.files[0];
//     if (file) {
//         appendMessage(`File: ${file.name}`, 'outgoing');
//     }
// });

// // Voice Recording Button (Web Speech API)
// // Voice Recording Button (Web Speech API)
// document.getElementById('recordBtn').addEventListener('click', () => {
//     const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
//     recognition.lang = 'ml-IN'; // Set language to Malayalam (India)
//     recognition.interimResults = false;

//     recognition.onstart = () => {
//         console.log('Voice recognition started.');
//     };

//     recognition.onresult = (event) => {
//         const transcript = event.results[0][0].transcript;
//         appendMessage(transcript, 'outgoing'); // Append the recognized text in Malayalam
//     };

//     recognition.onerror = (event) => {
//         console.error('Voice recognition error:', event.error);
//     };

//     recognition.start();
// });

// Function to send a message
document.getElementById('sendBtn').addEventListener('click', () => {
    const messageInput = document.getElementById('messageInput');
    const messageText = messageInput.value;

    if (messageText) {
        appendMessage(messageText, 'outgoing');
        messageInput.value = ''; // Clear input after sending

        // Send message to Django backend
        sendMessageToBackend(messageText);
    }
});

// Function to send message to the Django backend
function sendMessageToBackend(message) {
    fetch('/send-message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Ensure CSRF token is available
        },
        body: JSON.stringify({ message: message }),  // Use the correct variable 'message'
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received message:", data.message);
        if (data.message) {
            appendMessage(data.message, 'incoming'); // Append the response from Django
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}


// Function to append message to chat area
function appendMessage(text, type) {
    const chatArea = document.getElementById('chatArea');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', type);
    
    const messageContent = `
        <div class="message-content">
            <p>${text}</p>
            <span class="timestamp">${new Date().toLocaleTimeString()}</span>
        </div>`;
    
    messageDiv.innerHTML = messageContent;
    chatArea.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight; // Auto-scroll to bottom
}

// Function to get CSRF token (if using Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the given name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// File Attachment Button
document.getElementById('attachBtn').addEventListener('click', () => {
    document.getElementById('fileInput').click(); // Trigger file input
});

document.getElementById('fileInput').addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        appendMessage(`File: ${file.name}`, 'outgoing');
    }
});

// Voice Recording Button (Web Speech API)
document.getElementById('recordBtn').addEventListener('click', () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'ml-IN'; // Set language to Malayalam (India)
    recognition.interimResults = false;

    recognition.onstart = () => {
        console.log('Voice recognition started.');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        appendMessage(transcript, 'outgoing'); // Append the recognized text in Malayalam

        // Send the recognized text to Django backend
        sendMessageToBackend(transcript);
    };

    recognition.onerror = (event) => {
        console.error('Voice recognition error:', event.error);
    };

    recognition.start();
});
