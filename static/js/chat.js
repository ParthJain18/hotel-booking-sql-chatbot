const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const historyList = document.getElementById('historyList');
const newChatBtn = document.getElementById('newChatBtn');
const toggleSidebar = document.getElementById('toggleSidebar');
const chatSidebar = document.getElementById('chatSidebar');

// Current active chat history ID
let currentHistoryId = null;

// Function to add a message to the chat
function addMessage(message, isUser, responseTime = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-container';

    const messageContent = document.createElement('div');
    messageContent.className = isUser ? 'user-message' : 'bot-message';

    // Add avatar element
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = isUser ? '👤' : '🤖';
    messageContent.appendChild(avatar);

    // Add message content wrapper
    const contentWrapper = document.createElement('div');
    contentWrapper.className = 'message-content';

    // Add message text
    const textP = document.createElement('p');
    if (isUser) {
        textP.textContent = message;
    } else {
        textP.textContent = message.answer || "No answer provided";
    }
    contentWrapper.appendChild(textP);

    // If there's a SQL query, add it
    if (!isUser && message.sql) {
        const sqlDiv = document.createElement('div');
        sqlDiv.className = 'sql-query';
        sqlDiv.textContent = message.sql;
        contentWrapper.appendChild(sqlDiv);
    }

    // If there are images, add them
    if (!isUser && message.images) {
        message.images.forEach(image => {
            const imgElement = document.createElement('img');
            imgElement.src = `data:image/${image.format.toLowerCase()};base64,${image.data}`;
            contentWrapper.appendChild(imgElement);
        });
    }

    // Add response time if available
    if (responseTime) {
        const responseTimeDiv = document.createElement('div');
        responseTimeDiv.className = 'response-time';
        responseTimeDiv.textContent = `Response time: ${responseTime} ms`;
        contentWrapper.appendChild(responseTimeDiv);
    }

    messageContent.appendChild(contentWrapper);
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send the user's query to the server
async function sendQuery(query) {
    const userQuery = query || userInput.value.trim();
    if (!userQuery) return;

    addMessage(userQuery, true);
    userInput.value = '';
    userInput.focus();

    try {
        // Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message-container loading';
        loadingDiv.innerHTML = `
            <div class="bot-message">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <p>Thinking...</p>
                </div>
            </div>
        `;
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        const requestBody = { query: userQuery };
        if (currentHistoryId) {
            requestBody.history_id = currentHistoryId;
        }

        const startTime = Date.now();
        const response = await fetch('/chat/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        const endTime = Date.now();
        const responseTime = endTime - startTime;

        chatMessages.removeChild(loadingDiv);

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // If this is a new conversation, set the current history ID
        if (data.history_id && !currentHistoryId) {
            currentHistoryId = data.history_id;
            // Add to history list without reloading
            addHistoryToList({
                id: data.history_id,
                title: userQuery.substring(0, 30) + (userQuery.length > 30 ? "..." : ""),
                created_at: new Date().toISOString()
            });
        }

        addMessage(data, false, responseTime);
    } catch (error) {
        console.error("Error:", error);
        addMessage({ answer: `Error: ${error.message}`, sql: "" }, false);
    }
}

// Function to load a specific chat history
async function loadChatHistory(historyId) {
    try {
        const response = await fetch(`/chat/history/${historyId}`);

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const history = await response.json();

        // Clear current messages
        chatMessages.innerHTML = '';

        // Set current history ID
        currentHistoryId = history.id;

        // Add all messages from history
        history.messages.forEach(msg => {
            if (msg.is_user) {
                addMessage(msg.content, true);
            } else {
                addMessage(msg.content, false);
            }
        });

        // Update active class in sidebar
        document.querySelectorAll('.history-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`.history-item[data-id="${historyId}"]`).classList.add('active');
    } catch (error) {
        console.error("Error loading chat history:", error);
    }
}

// Function to start a new chat
function startNewChat() {
    // Clear current messages
    chatMessages.innerHTML = '';
    currentHistoryId = null;

    // Add welcome message
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'message-container';
    welcomeDiv.innerHTML = `
        <div class="bot-message">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <p>Hello! I'm your SQL assistant. Ask me questions about the hotel booking data.</p>
                <div class="message-examples">
                    <p>Try asking:</p>
                    <button class="example-btn" data-query="What other places can I visit near the hotel?">What other places can I visit near the hotel?</button>
                    <button class="example-btn" data-query="Generate a pie chart to show the cancelled bookings vs total">Generate a pie chart to show the cancelled bookings vs total</button>
                    <button class="example-btn" data-query="What's the average lead time for bookings?">What's the average lead time?</button>
                </div>
            </div>
        </div>
    `;
    chatMessages.appendChild(welcomeDiv);

    // Update active class in sidebar
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('active');
    });

    // Add example button event listeners
    document.querySelectorAll('.example-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            sendQuery(this.dataset.query);
        });
    });
}

// Function to add a history item to the list
function addHistoryToList(history) {
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item active';
    historyItem.dataset.id = history.id;
    historyItem.innerHTML = `
        <div class="history-title">${history.title}</div>
        <div class="history-date">${formatDate(history.created_at)}</div>
    `;

    // Remove active class from all others
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('active');
    });

    // Add to beginning of list
    if (historyList.firstChild) {
        historyList.insertBefore(historyItem, historyList.firstChild);
    } else {
        historyList.appendChild(historyItem);
    }

    // Add click event
    historyItem.addEventListener('click', () => {
        loadChatHistory(history.id);
    });
}

// Helper function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Event listeners
sendButton.addEventListener('click', () => sendQuery());
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendQuery();
    }
});

newChatBtn.addEventListener('click', startNewChat);

toggleSidebar.addEventListener('click', () => {
    chatSidebar.classList.toggle('hidden');
});

// Add event listeners to history items
document.querySelectorAll('.history-item').forEach(item => {
    item.addEventListener('click', function () {
        loadChatHistory(this.dataset.id);
    });
});

// Add event listeners to example buttons
document.querySelectorAll('.example-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        sendQuery(this.dataset.query);
    });
});

// Focus input on load
window.onload = function () {
    userInput.focus();
};
