from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string 


def sentiment_analysis(text, language):
    # Punctuation and stopwords
    punct = string.punctuation +'\n'
    stop_w = stopwords.words(language)

    # Text Preprocessing
    word_tokenized_text = word_tokenize(text.lower())
    filtered = [w for w in word_tokenized_text if (w.lower() not in punct and w.lower() not in stop_w) ]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered]
    processed_text = ' '.join(lemmatized_tokens)

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(processed_text)
    if -0.1 < scores['compound'] < 0.1: sentiment = "Neutral"
    else: sentiment = ":green[Positive]" if scores['compound'] > 0 else ":red[Negative]"
    return sentiment




