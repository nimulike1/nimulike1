document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // Function to add a message to the chatbox
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender + '-message');
        
        // If assistant message, might contain newlines that should be <br> or wrapped in <pre>
        if (sender === 'assistant') {
            const pre = document.createElement('pre');
            pre.textContent = text;
            messageDiv.appendChild(pre);
        } else {
            messageDiv.textContent = text;
        }
        
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to bottom
    }

    // Function to send command to backend
    async function sendCommand() {
        const commandText = userInput.value.trim();
        if (commandText === '') {
            return;
        }

        addMessage(commandText, 'user');
        userInput.value = ''; // Clear input field

        try {
            const response = await fetch('/process_command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: commandText }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                addMessage(`Error: ${errorData.error || response.statusText}`, 'assistant');
                return;
            }

            const data = await response.json();
            if (data.response) {
                addMessage(data.response, 'assistant');
            } else if (data.error) {
                addMessage(`Error: ${data.error}`, 'assistant');
            } else {
                addMessage('Received an empty response from the assistant.', 'assistant');
            }

        } catch (error) {
            console.error('Error sending command:', error);
            addMessage('There was an error connecting to the assistant. Please check the console.', 'assistant');
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendCommand);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendCommand();
        }
    });
});
