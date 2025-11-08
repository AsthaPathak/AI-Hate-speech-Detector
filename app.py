from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Load the model and vectorizer
model = joblib.load('hate_speech_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Initialize preprocessing tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()
        text = data.get('text', '')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Preprocess the text
        cleaned_text = preprocess_text(text)
        # Vectorize the text
        text_vector = tfidf_vectorizer.transform([cleaned_text])
        # Make prediction
        prediction = model.predict(text_vector)[0]
        # Get probability (confidence score)
        probability = model.predict_proba(text_vector)[0]

        # Map prediction to label
        label = "Hate Speech/Bullying" if prediction == 1 else "Safe"
        confidence = probability[1] if prediction == 1 else probability[0]

        # Return the result
        return jsonify({
            'label': label,
            'confidence': round(confidence, 4),
            'original_text': text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/moderate', methods=['POST'])
def moderate():
    """
    Endpoint for bulk moderation of multiple texts
    Expects: { "comments": [{"id": "unique_id", "text": "comment text"}, ...] }
    Returns: { "results": [{"id": "unique_id", "is_hate": bool, "confidence": float, "text": "..."}, ...] }
    """
    try:
        data = request.get_json()
        comments = data.get('comments', [])
        
        if not comments:
            return jsonify({'error': 'No comments provided'}), 400
        
        results = []
        for comment in comments:
            comment_id = comment.get('id', '')
            text = comment.get('text', '')
            
            if not text:
                results.append({
                    'id': comment_id,
                    'is_hate': False,
                    'confidence': 0,
                    'text': text,
                    'error': 'Empty text'
                })
                continue
            
            # Preprocess and predict
            cleaned_text = preprocess_text(text)
            text_vector = tfidf_vectorizer.transform([cleaned_text])
            prediction = model.predict(text_vector)[0]
            probability = model.predict_proba(text_vector)[0]
            
            is_hate = prediction == 1
            confidence = probability[1] if is_hate else probability[0]
            
            results.append({
                'id': comment_id,
                'is_hate': bool(is_hate),
                'confidence': round(float(confidence), 4),
                'text': text
            })
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Runs on http://127.0.0.1:5000