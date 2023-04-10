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
    # sentiment = "Positive" if scores['compound'] > 0 else "Negative"
    print(scores['compound'])
    print(scores)
    return sentiment

text_positive = """
CHAPTER!

Down the Rabbit-Hole

Alice was beginning to get very tired of sitting by her sister on the bank, and of having
nothing to do: once or twice she had peeped into the book her sister was reading, but
it had no pictures or conversations in it, "and what is the use of a book," thought Alice,
“without pictures or conversations?”

So she was considering in her own mind (as well as she could, for the hot day made
her feel very sleepy and stupid) whether the pleasure of making a daisy-chain would
be worth the trouble of getting up and picking the daisies, when suddenly a White
Rabbit with pink eyes ran close by her.

There was nothing so very remarkable in that; nor did Alice think it so very much out
of the way to hear the Rabbit say to itself, "Oh dear! Oh dear! | shall be too late!" (when
she thought it over afterwards, it occurred to her that she ought to have wondered at
this, but at the time it all seemed quite natural); but when the Rabbit actually took a
watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started
to her feet, for it flashed across her mind that she had never before seen a rabbit with
either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she
ran across the field after it, and was just in time to see it pop down a large rabbit-hole
under the hedge.

In another moment down went Alice after it, never once considering how in the world
she was to get out again."""

text_negative = """CHAPTER!

Down the fucking Rabbit-Hole

Alice was beginning to get very tired of sitting by her sister on the bank, and of having
nothing to do: once or twice she had peeped into the book her sister was fucking reading, but
it had no pictures or conversations in it, "and what is the use of a book," thought Alice,
“without pictures or conversations?”

So she was considering in her own fucking mind (as well as she could, for the hot day made
her feel very sleepy and stupid) whether the pleasure of making a daisy-chain would
be worth the fucking trouble of getting up and picking the daisies, when suddenly a White
Rabbit with pink eyes ran close by her.

Fuck this rabbit, said Alice.

There was nothing so very remarkable in that; nor did Alice think it so very much out
of the way to hear the Rabbit say to itself, "Oh dear! Oh dear! I shall be too late!" (when
she thought it over afterwards, it occurred to her that she ought to have wondered at
this, but at the time it all seemed quite natural); but when the Rabbit actually took a
watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started
to her feet, for it flashed across her mind that she had never before seen a rabbit with
either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she
ran across the field after it, and was just in time to see it pop down a large rabbit-hole
under the hedge.

Fuck this rabbit, she said again. I am going after that motherfucker!!!

In another moment down went Alice after it, never once considering how in the world
she was to get out again.

And there he was, the fucking rabbit. Alone in a pub taking a beer...
The bar was full of crackheads so she was feeling in danger but she never wanted to leave that fucking awful place...

Alice was not in wonderland, Alice was in drugs and kept saying:
"Fuck this rabbit!"
"Hate this rabbit!"
"Stupid rabbit!"
"""        

text_pt = "OLÁ, sou o João"


# print(sentiment_analysis(text_positive))
# print(sentiment_analysis(text_negative))
# print(sentiment_analysis(text_pt))




