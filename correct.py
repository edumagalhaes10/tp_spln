


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


def taxa_acerto(total_errors,total_sentences):
    if total_errors == 0:
       return 100
    ser = total_errors / total_sentences
    percent_correct = (1 - ser) * 100
    return percent_correct