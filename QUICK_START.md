# 🚀 Quick Start Guide

Get up and running in 3 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Download NLTK data:
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt')"
```

## Step 2: Start Flask Server

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

**Keep this terminal window open!**

## Step 3: Install Chrome Extension

1. Open Chrome and go to: `chrome://extensions/`
2. Enable **Developer mode** (top right toggle)
3. Click **"Load unpacked"**
4. Select the `chrome_extension` folder from this project
5. Done! Extension icon appears in toolbar

## Step 4: Test It Out

### Option A: Auto-Moderation (Recommended)
1. Visit any website with comments (Reddit, YouTube, Twitter, etc.)
2. Wait 2 seconds - extension auto-scans
3. Hate speech comments will be automatically blurred
4. Click "Show Content" to reveal if needed

### Option B: Manual Check
1. Select any text on a webpage
2. Click the extension icon (🛡️)
3. Click "✓ Check Selected Text"
4. See if it's Safe (green) or Hate Speech (red)

## ✅ Verification Checklist

- [ ] Flask server running (check terminal)
- [ ] Extension icon visible in Chrome toolbar
- [ ] Can open extension popup by clicking icon
- [ ] Auto-blur toggle is ON (green)
- [ ] No error messages in popup

## 🎮 Controls

**Extension Popup:**
- **Enable Auto-Blur** - Toggle automatic moderation on/off
- **🔍 Scan Page Now** - Manually scan current page
- **✓ Check Selected Text** - Check highlighted text

**On Blurred Comments:**
- **Show Content** - Reveal the blurred comment

## ⚠️ Common Issues

**"API Error - Is the Flask server running?"**
→ Start the Flask server with `python app.py`

**"Please refresh the page"**
→ Refresh the webpage (F5 or Ctrl+R)

**Comments not blurring**
→ Click "🔍 Scan Page Now" or wait for auto-scan

## 🎯 Test with Examples

Create a test HTML file to see it in action:

```html
<!DOCTYPE html>
<html>
<body>
  <h1>Test Comments</h1>
  <div class="comment">
    <p>This is a normal, friendly comment about cats.</p>
  </div>
  <div class="comment">
    <p>You are stupid and I hate you very much.</p>
  </div>
  <div class="comment">
    <p>Great article! Thanks for sharing.</p>
  </div>
</body>
</html>
```

Open this file in Chrome, and the extension should blur the hateful comment!

## 🔧 Adjust Sensitivity

Too many false positives? Edit `chrome_extension/contentScript.js`:

```javascript
const CONFIDENCE_THRESHOLD = 0.6; // Change to 0.7 or 0.8
```

Higher = stricter (fewer blurs, but might miss some hate speech)
Lower = more sensitive (more blurs, but might have false positives)

## 📱 Next Steps

- Read full [README.md](README.md) for detailed documentation
- Explore [app.py](app.py) to understand the ML model
- Check [train_model.py](train_model.py) to see how the model was trained
- Customize the blur effects in contentScript.js

---

**You're all set! 🎉 Browse safely!**
