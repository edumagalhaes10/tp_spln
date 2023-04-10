from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string 
from collections import Counter
from heapq import nlargest

# text = """I enjoy read book on sundays. It's relax and helps me to unwind from the stress of the week. I usually read fiction book, like the one about a detective who solve crime in a small town. The character are interesting and the plot is always full of surprises. Sometimes I read non-fiction book too, especially about science or history. I find it fascinating to learn about how thing work or about event that happened in the past. My only regret is that I don't have enough time to read as much as I want. Between work, family and other responsibilities, it can be difficult to find the time to indulge in my favorite pastime. He are moving here. I am doing fine. How is you? How is they? Matt like fish"""


def summarize(text, percentage, language):
    percentage = percentage / 100
    punct = string.punctuation +'\n'

    stop_w = stopwords.words(language)
    sent_tokenized_text = sent_tokenize(text)
    word_tokenized_text = word_tokenize(text)


    filtered = [w for w in word_tokenized_text if (w.lower() not in punct and w.lower() not in stop_w) ]
    word_count = Counter(filtered)
    # print(filtered)
    # print("-"*100)
    # print(word_count)

    max_occured_word = word_count.most_common(1)[0][1] 
    # print(max_occured_word)

    word_frequency = {}
    for word in word_count: 
        word_frequency[word] = word_count[word]/max_occured_word
    
    sentence_importance = {}
    for sent in sent_tokenized_text:
        for word in word_frequency:
            if word in sent.lower():
                if sent in sentence_importance: 
                    sentence_importance[sent] += word_frequency[word]
                else:
                    sentence_importance[sent] = word_frequency[word]

    # print(sentence_importance)

    summary = nlargest(int(len(sentence_importance)*percentage), sentence_importance, key = sentence_importance.get)
    print(" ".join(summary))
    return " ".join(summary)