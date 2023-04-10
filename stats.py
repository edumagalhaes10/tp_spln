import nltk
from collections import Counter
import string 



def stats(text):
    tokens = nltk.word_tokenize(text)
    text1 = nltk.Text(tokens)
    colocations = text1.collocation_list()
    # print(colocations)
    punct = string.punctuation +'\n'
    filtered = [w for w in tokens if w.lower() not in punct]
    most_used = Counter(filtered).most_common(10)
    # print(most_used.most_common(10)) 
    num_vocab = len(text1.vocab())
    md = f"""
### Vocabulary count: 
{num_vocab}

### Top 10 Most Used Words: 
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