// Status display
const statusDiv = document.getElementById('status');

function showStatus(message, duration = 3000) {
  statusDiv.textContent = message;
  statusDiv.style.display = 'block';
  setTimeout(() => {
    statusDiv.style.display = 'none';
  }, duration);
}

// Check Selected Text Button
document.getElementById('checkButton').addEventListener('click', async () => {
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = 'Analyzing...';
  resultDiv.className = '';
  
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: getSelectedText,
  }, (injectionResults) => {
    const selectedText = injectionResults[0]?.result;
    
    if (!selectedText) {
      resultDiv.textContent = "\u26A0 Please select some text first";
      resultDiv.className = "";
      return;
    }

    fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: selectedText })
    })
    .then(response => response.json())
    .then(data => {
      const confidencePercent = Math.round(data.confidence * 100);
      resultDiv.textContent = `${data.label === "Safe" ? "\u2713" : "\u26A0"} ${data.label} (${confidencePercent}%)`;
      resultDiv.className = data.label === "Safe" ? "safe" : "toxic";
      resultDiv.style.display = 'block';
    })
    .catch(error => {
      console.error('Error:', error);
      resultDiv.textContent = "\u274C API Error - Is the Flask server running?";
      resultDiv.className = "";
    });
  });
});

// Auto-Moderation Toggle
document.getElementById('autoModerationToggle').addEventListener('change', async (e) => {
  const enabled = e.target.checked;
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.tabs.sendMessage(tab.id, {
    action: 'toggleModeration',
    enabled: enabled
  }, (response) => {
    if (chrome.runtime.lastError) {
      showStatus('\u26A0 Please refresh the page');
      return;
    }
    showStatus(enabled ? '\u2713 Auto-moderation enabled' : '\u23F8 Auto-moderation paused');
  });
});

// Scan Page Now Button
document.getElementById('scanButton').addEventListener('click', async () => {
  const button = document.getElementById('scanButton');
  const originalText = button.textContent;
  button.textContent = '\u23F3 Scanning...';
  button.disabled = true;
  
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.tabs.sendMessage(tab.id, {
    action: 'scanNow'
  }, (response) => {
    button.textContent = originalText;
    button.disabled = false;
    
    if (chrome.runtime.lastError) {
      showStatus('\u26A0 Please refresh the page');
      return;
    }
    showStatus('\u2713 Page scanned successfully');
  });
});

// This function is executed inside the web page's context
function getSelectedText() {
  return window.getSelection().toString();
}

// Initialize - check if content script is loaded
document.addEventListener('DOMContentLoaded', async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  // Hide status initially
  statusDiv.style.display = 'none';
  
  chrome.tabs.sendMessage(tab.id, { action: 'ping' }, (response) => {
    if (chrome.runtime.lastError) {
      showStatus('\u2139 Refresh page to enable auto-moderation', 5000);
    }
  });
});