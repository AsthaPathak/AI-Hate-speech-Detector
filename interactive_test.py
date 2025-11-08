import joblib
import pandas as pd

# Load model
model = joblib.load('hate_speech_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

def preprocess_text(text):
    """Same preprocessing as before"""
    import re
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize
    
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    if not isinstance(text, str):
        return ""
    
    try:
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
        return ' '.join(tokens)
    except Exception:
        return ""

def test_custom_text():
    """Test your own custom text"""
    print("\n🎯 CUSTOM TEXT TESTING")
    print("Type 'quit' to exit\n")
    
    while True:
        text = input("Enter text to analyze: ").strip()
        
        if text.lower() == 'quit':
            break
            
        if not text:
            continue
            
        # Predict
        processed_text = preprocess_text(text)
        text_vector = tfidf_vectorizer.transform([processed_text])
        prediction = model.predict(text_vector)[0]
        confidence = model.predict_proba(text_vector)[0]
        
        predicted_label = "🚨 TOXIC" if prediction == 1 else "✅ SAFE"
        confidence_score = confidence[1] if prediction == 1 else confidence[0]
        
        print(f"Result: {predicted_label}")
        print(f"Confidence: {confidence_score:.4f}")
        print(f"Processed text: {processed_text}\n")

def show_dataset_samples():
    """Show some actual samples from your dataset"""
    df = pd.read_csv('train.csv')
    df['toxic'] = (df[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']].max(axis=1) > 0.5).astype(int)
    
    print("\n📊 DATASET SAMPLES:")
    print("Toxic examples:")
    toxic_samples = df[df['toxic'] == 1].sample(3)
    for _, row in toxic_samples.iterrows():
        print(f"  - {row['comment_text'][:100]}...")
    
    print("\nSafe examples:")
    safe_samples = df[df['toxic'] == 0].sample(3)
    for _, row in safe_samples.iterrows():
        print(f"  - {row['comment_text'][:100]}...")

if __name__ == "__main__":
    print("🤖 INTERACTIVE MODEL TESTER")
    show_dataset_samples()
    test_custom_text()