# 🔧 Troubleshooting Guide - Blur Not Working

## Quick Fix Checklist ✅

Follow these steps **in order**:

### Step 1: Install Missing Dependency
```bash
pip install flask-cors
```
✅ **This was missing and is now installed!**

### Step 2: Start Flask Server
```bash
cd c:\Users\Abhay\Documents\ai_moderator
python app.py
```

**Expected output:**
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

⚠️ **Keep this terminal window open!**

### Step 3: Reload Chrome Extension
1. Open Chrome: `chrome://extensions/`
2. Find "AI Hate Speech Moderator"
3. Click the **reload icon** (circular arrow)
4. **Grant permissions** if prompted for localhost access

### Step 4: Refresh Your Webpage
- Press `F5` or `Ctrl+R` to refresh the page
- Content script needs to reload to activate

### Step 5: Check Console Logs
1. Press `F12` to open DevTools
2. Go to **Console** tab
3. Look for: `AI Moderator: Auto-moderation enabled`
4. After 2 seconds: `AI Moderator: Found X comments to moderate`

---

## Common Issues & Solutions

### ❌ Issue 1: "flask-cors not installed"
**Symptom:** Server crashes on startup with ImportError

**Solution:**
```bash
pip install flask-cors
```

---

### ❌ Issue 2: No console logs appear
**Symptom:** Console is empty, no "AI Moderator" messages

**Solution:**
1. Extension not loaded properly
2. Go to `chrome://extensions/`
3. Click **Reload** button
4. **Refresh the webpage** (F5)

---

### ❌ Issue 3: "API Error" in console
**Symptom:** Console shows: `AI Moderator: API error 500`

**Solution:**
1. Check if Flask server is running
2. Restart Flask server: `python app.py`
3. Check for Python errors in terminal

---

### ❌ Issue 4: Comments not being detected
**Symptom:** Console shows "Found 0 comments"

**Solution:**
The content script looks for specific elements. Try:

1. **Manual scan**: Click extension icon → "🔍 Scan Page Now"
2. **Use test page**: Open `test_page.html` in Chrome
3. **Check page structure**: Some sites need custom selectors

---

### ❌ Issue 5: Blur not applying
**Symptom:** Console shows comments found, but no blur

**Possible causes:**
1. **Confidence too low** - Comments not hateful enough
2. **API not responding** - Check Flask terminal for errors
3. **CSS not injecting** - Check for style errors in console

**Solution:**
Lower confidence threshold in `contentScript.js`:
```javascript
const CONFIDENCE_THRESHOLD = 0.4; // Was 0.6
```

---

### ❌ Issue 6: Extension icon shows but popup doesn't work
**Symptom:** Clicking extension does nothing

**Solution:**
1. Check for JavaScript errors: Right-click extension icon → Inspect popup
2. Look for errors in popup console
3. Reload extension in `chrome://extensions/`

---

## Testing Procedure

### Test 1: Server is Running ✓

**Command:**
```bash
curl http://127.0.0.1:5000/predict -X POST -H "Content-Type: application/json" -d "{\"text\":\"you are stupid\"}"
```

**Expected:**
```json
{"label":"Hate Speech/Bullying","confidence":0.8234}
```

**Windows PowerShell Alternative:**
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:5000/predict -Method POST -ContentType "application/json" -Body '{"text":"you are stupid"}'
```

---

### Test 2: Extension Loaded ✓

1. Open: `chrome://extensions/`
2. Find: "AI Hate Speech Moderator"
3. Check: Toggle is **ON** (blue)
4. Check: No errors shown

---

### Test 3: Content Script Active ✓

1. Open test page: `file:///c:/Users/Abhay/Documents/ai_moderator/test_page.html`
2. Open Console (F12)
3. Within 2 seconds, see: `AI Moderator: Auto-moderation enabled`
4. After 2 seconds, see: `AI Moderator: Found X comments to moderate`

---

### Test 4: Blur Working ✓

On `test_page.html`:
- **3 comments** should be blurred (red tags)
- **5 comments** should be visible (green tags)
- Blurred ones show: "⚠️ Hate Speech Detected"
- Each has: "Show Content" button

---

## Debug Mode

### Enable Detailed Logging

Edit `contentScript.js`, add at top:
```javascript
const DEBUG_MODE = true;
```

Then add console logs:
```javascript
if (DEBUG_MODE) {
    console.log('Comments found:', comments.length);
    console.log('API Response:', data);
}
```

---

## Extension Console Logs

### How to View Content Script Logs

1. **Right-click** on the webpage (not extension icon)
2. Click **"Inspect"**
3. Go to **Console** tab
4. Filter by typing: `AI Moderator`

### How to View Popup Logs

1. **Right-click** extension icon
2. Click **"Inspect popup"**
3. Check Console tab in new DevTools window

---

## Network Tab Debugging

1. Open DevTools (F12)
2. Go to **Network** tab
3. Refresh page
4. Look for requests to: `127.0.0.1:5000/moderate`
5. Click on request → Check:
   - **Status**: Should be 200
   - **Response**: Should show results array
   - **Request**: Should show comments array

---

## Complete Reset Procedure

If nothing works, do a complete reset:

### 1. Stop Everything
- Close all Chrome tabs
- Stop Flask server (Ctrl+C)

### 2. Reinstall Dependencies
```bash
pip uninstall flask flask-cors
pip install -r requirements.txt
```

### 3. Verify Files
```bash
python -c "import flask, flask_cors; print('OK')"
```

### 4. Restart Flask
```bash
python app.py
```

### 5. Remove & Reload Extension
1. `chrome://extensions/`
2. **Remove** AI Moderator
3. **Load unpacked** → Select `chrome_extension` folder
4. **Grant permissions** when prompted

### 6. Test with Test Page
1. Open `test_page.html`
2. Open Console (F12)
3. Wait 3 seconds
4. Check for blurred comments

---

## Still Not Working?

### Check These Files Exist:
```
✓ hate_speech_model.pkl
✓ tfidf_vectorizer.pkl
✓ chrome_extension/contentScript.js
✓ chrome_extension/popup.html
✓ chrome_extension/popup.js
✓ chrome_extension/manifest.json
```

### Check Flask Terminal for Errors:
Look for:
- `ModuleNotFoundError`
- `FileNotFoundError`
- `PermissionError`
- API call logs (should see POST requests)

### Check Chrome Console for Errors:
Look for:
- `Failed to fetch`
- `CORS error`
- `Uncaught TypeError`
- `Extension context invalidated`

---

## Manual Testing Script

Run this in the Chrome Console (on any webpage):

```javascript
// Test API connection
fetch('http://127.0.0.1:5000/moderate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        comments: [
            {id: 'test1', text: 'You are stupid and I hate you'},
            {id: 'test2', text: 'This is a nice comment'}
        ]
    })
})
.then(r => r.json())
.then(d => console.log('API Response:', d))
.catch(e => console.error('API Error:', e));
```

**Expected output:**
```javascript
API Response: {
  results: [
    {id: 'test1', is_hate: true, confidence: 0.8+},
    {id: 'test2', is_hate: false, confidence: 0.9+}
  ]
}
```

---

## Permissions Issue (Chrome)

If Chrome blocks localhost access:

1. Extension permissions might not be granted
2. Check: `chrome://extensions/` → AI Moderator → "Details"
3. Scroll to "Site access"
4. Should show: "On specific sites"
5. Check host_permissions in manifest.json

---

## Performance Tips

If extension is slow:

1. **Increase scan interval** (less frequent scans):
   ```javascript
   setInterval(scanPage, 30000); // 30 seconds instead of 10
   ```

2. **Increase text length threshold** (fewer items to check):
   ```javascript
   if (text.length >= 50 && text.length <= 2000) // Was 10
   ```

3. **Disable auto-scan** (manual only):
   - Toggle "Enable Auto-Blur" to OFF
   - Use "Scan Page Now" button when needed

---

## Success Indicators

When everything works:

### Flask Terminal:
```
127.0.0.1 - - [date] "POST /moderate HTTP/1.1" 200 -
```

### Chrome Console:
```
AI Moderator: Auto-moderation enabled
AI Moderator: Found 8 new comments to moderate
```

### Webpage:
- Blurred comments with red warnings
- "Show Content" buttons visible
- Can click to reveal

---

## Contact / Report Issues

If you've tried everything:

1. Check Flask terminal output
2. Check Chrome console output
3. Try `test_page.html`
4. Check if model files exist
5. Verify Python version (3.8+)

---

**Last Updated:** After fixing flask-cors issue
**Status:** ✅ Dependencies installed, manifest updated
