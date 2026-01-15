// Interactive SRS Generator - Client-side JavaScript

let sessionId = null;
let isProcessing = false;
let generatedSRS = null;

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const completionPanel = document.getElementById('completionPanel');
const downloadButton = document.getElementById('downloadButton');

// Initialize the chat session when page loads
document.addEventListener('DOMContentLoaded', () => {
    startInteractiveSession();
    
    chatForm.addEventListener('submit', handleUserMessage);
    downloadButton.addEventListener('click', downloadSRS);
});

/**
 * Start a new interactive session with the AI agent
 */
async function startInteractiveSession() {
    try {
        showTypingIndicator();
        
        const response = await fetch('/api/v1/interactive/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        hideTypingIndicator();
        
        if (response.ok) {
            sessionId = data.session_id;
            addAgentMessage(data.message);
            updateProgress(data.progress);
        } else {
            addErrorMessage('Failed to start session: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        hideTypingIndicator();
        addErrorMessage('Connection error: ' + error.message);
    }
}

/**
 * Handle user message submission
 */
async function handleUserMessage(e) {
    e.preventDefault();
    
    if (isProcessing || !userInput.value.trim()) {
        return;
    }
    
    const message = userInput.value.trim();
    userInput.value = '';
    
    // Add user message to chat
    addUserMessage(message);
    
    // Send to agent
    await sendMessageToAgent(message);
}

/**
 * Send user message to the agent API
 */
async function sendMessageToAgent(message) {
    if (!sessionId) {
        addErrorMessage('No active session. Please refresh the page.');
        return;
    }
    
    isProcessing = true;
    sendButton.disabled = true;
    userInput.disabled = true;
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/v1/interactive/respond', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });
        
        const data = await response.json();
        
        hideTypingIndicator();
        
        if (response.ok) {
            if (data.status === 'complete') {
                // Session is complete
                addAgentMessage(data.message);
                updateProgress(data.progress);
                handleCompletion(data.sections);
            } else {
                // Continue conversation
                addAgentMessage(data.message);
                updateProgress(data.progress);
            }
        } else {
            addErrorMessage('Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        hideTypingIndicator();
        addErrorMessage('Connection error: ' + error.message);
    } finally {
        isProcessing = false;
        sendButton.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

/**
 * Add an agent message to the chat
 */
function addAgentMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = formatMessage(message);
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

/**
 * Add a user message to the chat
 */
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

/**
 * Add an error message to the chat
 */
function addErrorMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.style.background = '#ffebee';
    contentDiv.style.borderColor = '#ef5350';
    contentDiv.style.color = '#c62828';
    // Use textContent to prevent XSS
    contentDiv.textContent = '⚠️ ' + message;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    let indicator = document.getElementById('typingIndicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'typingIndicator';
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(indicator);
    }
    indicator.classList.add('active');
    scrollToBottom();
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.remove('active');
    }
}

/**
 * Update progress bar
 */
function updateProgress(progress) {
    if (!progress) return;
    
    const percentage = progress.percentage || 0;
    progressFill.style.width = percentage + '%';
    progressText.textContent = percentage + '% Complete';
    
    if (percentage >= 100) {
        progressFill.style.background = '#4CAF50';
    }
}

/**
 * Handle completion of the interactive session
 */
function handleCompletion(sections) {
    generatedSRS = sections;
    
    // Disable input
    chatForm.style.display = 'none';
    
    // Show completion panel
    completionPanel.classList.add('active');
    
    // Add a final message
    setTimeout(() => {
        addAgentMessage('🎉 Your SRS document is ready! Click the button below to download it.');
    }, 1000);
}

/**
 * Download the generated SRS document
 */
function downloadSRS() {
    if (!generatedSRS) {
        // Show error in chat instead of alert
        addErrorMessage('No SRS document available to download.');
        return;
    }
    
    const sections = generatedSRS;
    const markdown = buildMarkdownDocument(sections);
    
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    const timestamp = new Date().toISOString().split('T')[0];
    a.href = url;
    a.download = `srs_document_${timestamp}.md`;
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Build complete markdown document from sections
 */
function buildMarkdownDocument(sections) {
    let markdown = '# Software Requirements Specification\n\n';
    markdown += `*Generated on: ${new Date().toLocaleDateString()}*\n\n`;
    markdown += '---\n\n';
    
    if (sections.introduction) {
        markdown += '## 1. Introduction\n\n';
        markdown += sections.introduction + '\n\n';
    }
    
    if (sections.system_description) {
        markdown += '## 2. System Description\n\n';
        markdown += sections.system_description + '\n\n';
    }
    
    if (sections.functional_requirements) {
        markdown += '## 3. Functional Requirements\n\n';
        markdown += sections.functional_requirements + '\n\n';
    }
    
    if (sections.non_functional_requirements) {
        markdown += '## 4. Non-Functional Requirements\n\n';
        markdown += sections.non_functional_requirements + '\n\n';
    }
    
    if (sections.user_interface) {
        markdown += '## 5. User Interface Requirements\n\n';
        markdown += sections.user_interface + '\n\n';
    }
    
    if (sections.constraints) {
        markdown += '## 6. System Constraints\n\n';
        markdown += sections.constraints + '\n\n';
    }
    
    markdown += '---\n\n';
    markdown += '*Generated by Interactive SRS Generator*\n';
    
    return markdown;
}

/**
 * Escape HTML to prevent XSS attacks
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format message text with basic markdown support
 * Escapes HTML to prevent XSS while allowing safe markdown formatting
 */
function formatMessage(text) {
    if (!text) return '';
    
    // First escape HTML to prevent XSS
    let formatted = escapeHtml(text);
    
    // Then apply markdown formatting
    formatted = formatted
        // Bold
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        // Line breaks
        .replace(/\n/g, '<br>');
    
    return formatted;
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
