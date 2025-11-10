const API_URL = 'http://localhost:8080';

const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');


let conversationHistory = [];


conversationHistory.forEach(msg => {
    addMessageToChat(msg.message, msg.isUser);
});

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessageToChat(message, true);
    conversationHistory.push({ message, isUser: true });
    
    // Clear input
    messageInput.value = '';
    
    // Disable send button and show typing indicator
    sendButton.disabled = true;
    typingIndicator.style.display = 'flex';
    
    try {
        // Send message to API
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                conversation_history: conversationHistory 
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Add bot response to chat
        addMessageToChat(data.response, false);

        
        conversationHistory = data.conversation_history;
        
        
        // localStorage.setItem('hr_chat_history', JSON.stringify(conversationHistory));
        
    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('Xin lỗi, đã có lỗi xảy ra khi kết nối tới server. Vui lòng thử lại sau.', false);
    } finally {
        // Enable send button and hide typing indicator
        sendButton.disabled = false;
        typingIndicator.style.display = 'none';
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});

function addMessageToChat(message, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (!isUser) {
        const headerDiv = document.createElement('div');
        headerDiv.className = 'message-header';
        headerDiv.innerHTML = '<span class="bot-avatar">🤖</span><span class="message-author">HR Bot</span>';
        contentDiv.appendChild(headerDiv);
    }
    
    const messageText = formatMessage(message);
    contentDiv.appendChild(messageText);
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function formatMessage(text) {
    const container = document.createElement('div');
    const lines = text.split('\n');
    
    lines.forEach(line => {
        if (line.trim() === '') {
            container.appendChild(document.createElement('br'));
        } else if (line.trim().startsWith('- ') || line.trim().startsWith('• ')) {
            const listItem = document.createElement('div');
            listItem.textContent = line.trim();
            listItem.style.marginLeft = '20px';
            container.appendChild(listItem);
        } else if (line.trim().match(/^\d+\./)) {
            const listItem = document.createElement('div');
            listItem.textContent = line.trim();
            listItem.style.marginLeft = '20px';
            container.appendChild(listItem);
        } else {
            const paragraph = document.createElement('p');
            paragraph.textContent = line.trim();
            container.appendChild(paragraph);
        }
    });
    
    return container;
}

messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
});

messageInput.focus();