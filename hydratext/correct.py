
from nltk.tokenize import sent_tokenize


def highlight_sentence(phrase,edits):
   words = phrase.split()
   for edit in edits:
      print(edit,words)
      while len(words) <= edit[2]:
         words.append("")
      if edit[2] == edit[3]:
         # add word between edit[2] and edit[3]
         words = words[:edit[2]] + [""] + words[edit[2]:]
      words[edit[2]] = f'~~:red[{edit[1]}]~~ :green[{edit[4]}]'
      if edit[3] - edit[2] >= 2:
         for n in range(edit[2] + 1, edit[3]):
            words[n] = ""
   return " ".join(words)

def correct_sentence(sentence, gramformer):
    total_errors = 0
    corrected_sentences = gramformer.correct(sentence, max_candidates=1)
    for corrected_sentence in corrected_sentences:
       if corrected_sentence != sentence:
           total_errors += 1
       edits = gramformer.get_edits(sentence, corrected_sentence)
       raw = corrected_sentence
       correcao = highlight_sentence(sentence,edits)
    return correcao,raw, total_errors


def add_newlines(sentence, indices):
   word_tokens = sentence.split(" ")
   for index in indices:
      word_tokens = word_tokens[:index] + ["  \n"] + word_tokens[index:]
   sentence = " ".join(word_tokens)
   return sentence



def grammar_correct(influent_sentence,progress_bar,gramformer):
   sentences = sent_tokenize(influent_sentence)
   total_sentences = len(sentences)
   total_errors = 0
   progress = 1/total_sentences
   raw = ""
   correcao = ""
   for i, sent in enumerate(sentences):
      word_tokens = sent.split(" ")
      new_word_tokens = []
      for word in word_tokens:
         if "\n" in word:
            l = word.split("\n")
            for w in l:
               new_word_tokens.append(w)
               new_word_tokens.append("\n")
            new_word_tokens = new_word_tokens[:-1]
         else:
            new_word_tokens.append(word)
      word_tokens = new_word_tokens
      indices = [j for j, x in enumerate(word_tokens) if x == "\n"]
      correct_sent, raw_sent, erros_sent = correct_sentence(sent, gramformer)
      correct_sent = add_newlines(correct_sent, indices)
      raw_sent = add_newlines(raw_sent, indices)
      total_errors += erros_sent
      correcao += " " + correct_sent
      raw += " " + raw_sent
      progress_bar.progress((i+1) / total_sentences)
      progress_bar.progress(progress * (i+1))
   taxa = taxa_acerto(total_errors,total_sentences)
   return correcao,raw




def taxa_acerto(total_errors,total_sentences):
    if total_errors == 0:
       return 100
    ser = total_errors / total_sentences
    percent_correct = (1 - ser) * 100
    return percent_correct