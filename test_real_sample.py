import pandas as pd
import joblib
import random

# Load everything
model = joblib.load('hate_speech_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
df = pd.read_csv('train.csv')

# Create target
df['toxic'] = (df[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']].max(axis=1) > 0.5).astype(int)

def test_real_samples():
    """Test actual samples from your dataset"""
    print("Testing real dataset samples...\n")
    
    # Get some toxic and safe samples
    toxic_samples = df[df['toxic'] == 1].sample(10)
    safe_samples = df[df['toxic'] == 0].sample(10)
    
    print("🚨 TOXIC COMMENTS PREDICTIONS:")
    correct_toxic = 0
    for idx, row in toxic_samples.iterrows():
        text = row['comment_text']
        processed_text = preprocess_text(text)
        text_vector = tfidf_vectorizer.transform([processed_text])
        prediction = model.predict(text_vector)[0]
        
        result = "✅ Correct" if prediction == 1 else "❌ Wrong"
        if prediction == 1:
            correct_toxic += 1
            
        print(f"{result}: {text[:80]}...")
    
    print(f"\n📊 Toxic detection accuracy: {correct_toxic}/10")
    
    print("\n✅ SAFE COMMENTS PREDICTIONS:")
    correct_safe = 0
    for idx, row in safe_samples.iterrows():
        text = row['comment_text']
        processed_text = preprocess_text(text)
        text_vector = tfidf_vectorizer.transform([processed_text])
        prediction = model.predict(text_vector)[0]
        
        result = "✅ Correct" if prediction == 0 else "❌ Wrong"
        if prediction == 0:
            correct_safe += 1
            
        print(f"{result}: {text[:80]}...")
    
    print(f"\n📊 Safe detection accuracy: {correct_safe}/10")
    print(f"🎯 Overall accuracy: {(correct_toxic + correct_safe)/20:.1%}")

# Include the same preprocessing function
def preprocess_text(text):
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

if __name__ == "__main__":
    test_real_samples()