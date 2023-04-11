import nltk
from collections import Counter
import string 
from nltk.corpus import stopwords



def stats(text, language):
    tokens = nltk.word_tokenize(text)
    punct = string.punctuation +'\n' +'”'+"“"
    stop_w = stopwords.words(language)
    filtered = [w for w in tokens if w.lower() not in punct]
    filtered2 = [w for w in tokens if w.lower() not in stop_w and w.lower() not in punct and w.lower() not in ['\'s']]

    text1 = nltk.Text(filtered)
    text2 = nltk.Text(tokens)
    colocations = text2.collocation_list()
    # print(colocations)
    most_used_no_stop = Counter(filtered2).most_common(10)
    most_used = Counter(tokens).most_common(10)
    # print(most_used.most_common(10)) 
    num_vocab = len(text1.vocab())
    print(text1.vocab())
    md = f"""
### Vocabulary count: 
{num_vocab}

### Top 10 Most Used Words: 
> Words that are not stopwords and punctuation.

| Word                                    | Frequency                               | 
| --------------------------------------- | --------------------------------------- |
"""

    for w in most_used_no_stop:
        md+=f"""| {w[0]} | {w[1]} |\n"""   
    md+="""
---

> No restrictions.

| Word                                    | Frequency                               |
| --------------------------------------- | --------------------------------------- |
"""
    for w in most_used:
        md+=f"""| {w[0]} | {w[1]} |\n"""
    md+="""
### Colocations:
> A sequence of words that occurs together unusually often.

"""
    if colocations:
        for word in colocations:
            md += f"- {word[0]} {word[1]}\n"
    else:
        md += "No colocations found."
    print(md)
    return md