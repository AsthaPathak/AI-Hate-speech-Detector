// AI Moderator Content Script - Auto-scans and blurs hate speech

console.log("AI Moderator: Auto-moderation enabled");

const API_URL = 'http://127.0.0.1:5000/moderate';
const CONFIDENCE_THRESHOLD = 0.6; // Only blur if confidence > 60%
let moderationEnabled = true;
let processedComments = new Set();

// Inject blur styles
const style = document.createElement('style');
style.textContent = `
    .ai-moderator-blurred {
        filter: blur(8px);
        opacity: 0.5;
        transition: all 0.3s ease;
        position: relative;
        user-select: none;
        cursor: pointer;
    }
    
    .ai-moderator-container {
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .ai-moderator-warning {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(220, 38, 38, 0.95);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: bold;
        pointer-events: none;
        z-index: 1000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .ai-moderator-reveal-btn {
        display: block;
        margin-top: 8px;
        padding: 6px 12px;
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 11px;
        cursor: pointer;
        font-weight: 500;
        transition: background 0.2s;
    }
    
    .ai-moderator-reveal-btn:hover {
        background: #2563eb;
    }
    
    .ai-moderator-revealed {
        filter: none !important;
        opacity: 1 !important;
        user-select: text !important;
    }
`;
document.head.appendChild(style);

// Function to get selected text (for manual checking)
function getSelectedText() {
    return window.getSelection().toString().trim();
}

// Generate unique ID for comments
function generateCommentId(element) {
    const text = element.textContent.trim();
    return btoa(text.substring(0, 50)).replace(/[^a-zA-Z0-9]/g, '');
}

// Find all text elements that could be comments
function findComments() {
    const selectors = [
        'p', 'div[class*="comment"]', 'div[class*="post"]', 
        'div[class*="message"]', 'span[class*="text"]',
        'article', 'div[role="article"]', 'li[class*="comment"]',
        '[data-testid*="comment"]', '[data-testid*="post"]'
    ];
    
    const elements = [];
    selectors.forEach(selector => {
        const found = document.querySelectorAll(selector);
        found.forEach(el => {
            const text = el.textContent.trim();
            // Only process elements with substantial text (10-2000 chars)
            if (text.length >= 10 && text.length <= 2000) {
                const id = generateCommentId(el);
                if (!processedComments.has(id)) {
                    elements.push({ element: el, id, text });
                }
            }
        });
    });
    
    return elements;
}

// Send comments to API for moderation
async function moderateComments(comments) {
    if (comments.length === 0) return;
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                comments: comments.map(c => ({ id: c.id, text: c.text }))
            })
        });
        
        if (!response.ok) {
            console.error('AI Moderator: API error', response.status);
            return;
        }
        
        const data = await response.json();
        applyModeration(data.results, comments);
    } catch (error) {
        console.error('AI Moderator: Failed to moderate comments', error);
    }
}

// Apply blur effect to hate speech comments
function applyModeration(results, comments) {
    results.forEach(result => {
        if (result.is_hate && result.confidence >= CONFIDENCE_THRESHOLD) {
            const comment = comments.find(c => c.id === result.id);
            if (comment && comment.element) {
                blurComment(comment.element, result);
                processedComments.add(result.id);
            }
        }
    });
}

// Blur a single comment
function blurComment(element, result) {
    // Skip if already blurred
    if (element.classList.contains('ai-moderator-blurred')) return;
    
    // Create container wrapper
    const container = document.createElement('div');
    container.className = 'ai-moderator-container';
    
    // Wrap the element
    element.parentNode.insertBefore(container, element);
    container.appendChild(element);
    
    // Add blur effect
    element.classList.add('ai-moderator-blurred');
    
    // Add warning label
    const warning = document.createElement('div');
    warning.className = 'ai-moderator-warning';
    warning.textContent = `\u26A0 Hate Speech Detected (${Math.round(result.confidence * 100)}%)`;
    container.appendChild(warning);
    
    // Add reveal button
    const revealBtn = document.createElement('button');
    revealBtn.className = 'ai-moderator-reveal-btn';
    revealBtn.textContent = 'Show Content';
    revealBtn.onclick = (e) => {
        e.stopPropagation();
        element.classList.add('ai-moderator-revealed');
        warning.style.display = 'none';
        revealBtn.textContent = 'Content Revealed';
        revealBtn.disabled = true;
        revealBtn.style.background = '#6b7280';
    };
    container.appendChild(revealBtn);
}

// Auto-scan page for comments
function scanPage() {
    if (!moderationEnabled) return;
    
    const comments = findComments();
    if (comments.length > 0) {
        console.log(`AI Moderator: Found ${comments.length} new comments to moderate`);
        moderateComments(comments);
    }
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "ping") {
        sendResponse({ success: true, status: "ready" });
    } else if (request.action === "getSelectedText") {
        const selectedText = getSelectedText();
        sendResponse({ text: selectedText });
    } else if (request.action === "toggleModeration") {
        moderationEnabled = request.enabled;
        if (moderationEnabled) {
            scanPage();
        }
        sendResponse({ success: true, enabled: moderationEnabled });
    } else if (request.action === "scanNow") {
        processedComments.clear();
        scanPage();
        sendResponse({ success: true });
    }
    return true;
});

// Initial scan
setTimeout(scanPage, 2000);

// Periodic scan for new comments (every 10 seconds)
setInterval(scanPage, 10000);

// Observe DOM changes for dynamically loaded content
const observer = new MutationObserver((mutations) => {
    let shouldScan = false;
    mutations.forEach(mutation => {
        if (mutation.addedNodes.length > 0) {
            shouldScan = true;
        }
    });
    if (shouldScan && moderationEnabled) {
        setTimeout(scanPage, 1000);
    }
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});