# 🛡️ AI Hate Speech Moderator

An intelligent Chrome extension that automatically detects and **blurs hate speech** and cyberbullying comments in real-time across all websites.

## ✨ Features

### 🔄 Automatic Moderation
- **Auto-scan**: Continuously monitors web pages for new comments
- **Smart Detection**: Uses ML model trained on hate speech patterns
- **Blur Effect**: Automatically blurs detected hate speech with visual warning
- **Reveal Option**: Users can choose to reveal blurred content
- **Real-time**: Scans dynamically loaded content (AJAX/SPA support)

### 🎯 Manual Checking
- Select any text on a webpage
- Get instant hate speech classification
- View confidence scores

### 🎨 Modern UI
- Beautiful gradient design
- Toggle auto-moderation on/off
- Manual page scan button
- Clear visual indicators for safe/toxic content

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Google Chrome browser
- Flask server running locally

### Backend Setup

1. **Clone/Navigate to the project directory**
   ```bash
   cd ai_moderator
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (if not already downloaded)
   ```python
   python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt')"
   ```

4. **Start the Flask server**
   ```bash
   python app.py
   ```
   
   The server will run on `http://127.0.0.1:5000`

### Chrome Extension Setup

1. **Open Chrome Extensions page**
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)

2. **Load the extension**
   - Click "Load unpacked"
   - Select the `chrome_extension` folder

3. **Verify installation**
   - Extension icon should appear in Chrome toolbar
   - Click it to open the control panel

## 📖 Usage

### Auto-Moderation (Recommended)

1. **Ensure Flask server is running** (`python app.py`)
2. **Navigate to any webpage** with comments (Reddit, YouTube, Twitter, etc.)
3. **Extension automatically scans** the page after 2 seconds
4. **Hate speech comments are blurred** with a warning overlay
5. **Click "Show Content"** button to reveal if needed

### Manual Text Checking

1. **Select any text** on a webpage
2. **Click the extension icon** in Chrome toolbar
3. **Click "✓ Check Selected Text"**
4. **View the result**: Safe (green) or Hate Speech/Bullying (red)

### Controls

- **Enable Auto-Blur Toggle**: Turn auto-moderation on/off
- **🔍 Scan Page Now**: Manually trigger a full page scan
- **Show Content Button**: Reveal individual blurred comments

## 🔧 Configuration

### Adjust Detection Sensitivity

Edit `chrome_extension/contentScript.js`:

```javascript
const CONFIDENCE_THRESHOLD = 0.6; // Default: 60%
// Increase for fewer false positives (stricter)
// Decrease for more comprehensive detection (broader)
```

### Modify Scan Intervals

```javascript
// Initial scan delay (default: 2 seconds)
setTimeout(scanPage, 2000);

// Periodic scan interval (default: 10 seconds)
setInterval(scanPage, 10000);
```

### Customize Blur Appearance

Edit the CSS in `contentScript.js` style block:

```css
.ai-moderator-blurred {
    filter: blur(8px);  /* Adjust blur intensity */
    opacity: 0.5;       /* Adjust transparency */
}
```

## 🏗️ Project Structure

```
ai_moderator/
├── app.py                      # Flask backend with ML model
├── requirements.txt            # Python dependencies
├── hate_speech_model.pkl       # Trained ML model
├── tfidf_vectorizer.pkl        # TF-IDF vectorizer
├── train_model.py              # Model training script
├── chrome_extension/
│   ├── manifest.json           # Extension configuration
│   ├── popup.html              # Extension UI
│   ├── popup.js                # UI logic
│   └── contentScript.js        # Content scanning & blur logic
└── README.md                   # This file
```

## 🔬 How It Works

### Backend (Flask)
1. **ML Model**: Trained on hate speech dataset
2. **Preprocessing**: Tokenization, lemmatization, stopword removal
3. **Classification**: TF-IDF vectorization + ML prediction
4. **API Endpoints**:
   - `/predict` - Single text classification
   - `/moderate` - Bulk comment moderation

### Frontend (Chrome Extension)
1. **Content Script**: Scans DOM for comment-like elements
2. **Batch Processing**: Sends comments to Flask API
3. **Smart Filtering**: Only processes 10-2000 character texts
4. **Visual Effects**: Applies blur + warning overlay to hate speech
5. **User Control**: Toggle, manual scan, reveal buttons

### Detection Pipeline
```
Web Page → Find Comments → Send to API → ML Classification 
   → If Hate Speech → Apply Blur + Warning → User Can Reveal
```

## 🎯 API Endpoints

### POST `/predict`
Single text classification

**Request:**
```json
{
  "text": "Your comment here"
}
```

**Response:**
```json
{
  "label": "Safe" | "Hate Speech/Bullying",
  "confidence": 0.8542,
  "original_text": "Your comment here"
}
```

### POST `/moderate`
Bulk comment moderation

**Request:**
```json
{
  "comments": [
    {"id": "comment1", "text": "First comment"},
    {"id": "comment2", "text": "Second comment"}
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "comment1",
      "is_hate": false,
      "confidence": 0.92,
      "text": "First comment"
    },
    {
      "id": "comment2",
      "is_hate": true,
      "confidence": 0.87,
      "text": "Second comment"
    }
  ]
}
```

## 🐛 Troubleshooting

### Extension shows "API Error"
- **Ensure Flask server is running**: `python app.py`
- **Check server address**: Must be `http://127.0.0.1:5000`
- **Check console logs**: Open DevTools → Console

### Comments not being blurred
- **Refresh the page** after installing extension
- **Check if auto-blur is enabled** (toggle in extension popup)
- **Manually scan**: Click "🔍 Scan Page Now"
- **Adjust confidence threshold** if too strict

### "Please refresh the page" message
- The content script needs to be reloaded
- Simply **refresh the webpage** (F5 or Ctrl+R)

### Performance issues
- **Reduce scan frequency**: Edit `setInterval` in contentScript.js
- **Increase text length threshold**: Modify `text.length >= 10` condition
- **Disable on heavy pages**: Toggle off auto-moderation

## 🔒 Privacy & Security

- ✅ All processing happens **locally** (your machine)
- ✅ No data sent to external servers
- ✅ Comments only sent to localhost Flask API
- ✅ No personal data collection or storage
- ✅ Open source - audit the code yourself

## 📊 Model Information

- **Training Data**: Hate speech and cyberbullying dataset
- **Algorithm**: TF-IDF + Classification (specific algorithm depends on train_model.py)
- **Features**: Text preprocessing with lemmatization and stopword removal
- **Confidence Threshold**: 60% (configurable)

## 🛠️ Development

### Testing the Model
```bash
python test_model.py          # Test with predefined samples
python interactive_test.py     # Interactive testing
python test_real_sample.py     # Real-world examples
```

### Retraining the Model
```bash
python train_model.py          # Retrain with train.csv
```

## 📝 License

This project is for educational and research purposes.

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve the ML model

## ⚠️ Disclaimer

This tool uses machine learning and may not be 100% accurate. False positives and false negatives can occur. Use as a supplementary tool, not a definitive solution.

## 📧 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Chrome DevTools console logs
3. Check Flask server logs
4. Open an issue on the project repository

---

**Made with ❤️ to make the internet a safer place**
