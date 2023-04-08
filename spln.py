import streamlit as st
import pandas as pd
import pytesseract
from io import StringIO
from PIL import Image
from summarize_text import summarize
from correct import correct_sentence, taxa_acerto
from gramformer import Gramformer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
import re 


#Session State

if 'gramformer' not in st.session_state:
   st.session_state.gramformer = Gramformer(models = 1, use_gpu=False)

if 'action' not in st.session_state:
   st.session_state.action = None

if 'out' not in st.session_state:
   st.session_state.out = None

if 'changed' not in st.session_state:
   st.session_state.changed = True

if 'genre' not in st.session_state:
   st.session_state.genre = None


def grammar_correct(influent_sentence):
   st.write("Checking grammar...")
   progress_bar = st.progress(0)
   #sentences = LineTokenizer(blanklines='keep').tokenize(influent_sentence)
   sentences = sent_tokenize(influent_sentence)
   total_sentences = len(sentences)
   total_errors = 0
   progress = 1/total_sentences
   raw = ""
   correcao = ""
   for i, sent in enumerate(sentences):
      #sent = sent.replace('\n', "  ")
      #word_tokens = word_tokenize(sent,preserve_line=True)
      print(f'SENTENCE = {sent}')
      word_tokens = sent.split(" ")
      print(f'WORD TOKENS = {word_tokens}')
      new_word_tokens = []
      for j, word in enumerate(word_tokens):
         if "\n" in word:
            l = word.split("\n")
            for w in l:
               new_word_tokens.append(w)
               new_word_tokens.append("\n")
            new_word_tokens = new_word_tokens[:-1]
         else:
            new_word_tokens.append(word)
      word_tokens = new_word_tokens
      print(f'WORD TOKENS = {word_tokens}')
      indices = [j for j, x in enumerate(word_tokens) if x == "\n"]
      print(f'INDICES = {indices}')
      correct_sent, raw_sent, erros_sent = correct_sentence(sent, st.session_state.gramformer)
      #correct_sent, raw_sent = correct_sent.replace("  ",'  \n'), raw_sent.replace("  ",'  \n')
      correct_word_tokens = correct_sent.split(" ")
      correct_word_tokens_raw = raw_sent.split(" ")
      for index in indices:
         correct_word_tokens = correct_word_tokens[:index] + ["  \n"] + correct_word_tokens[index:]
         correct_word_tokens_raw = correct_word_tokens_raw[:index] + ["  \n"] + correct_word_tokens_raw[index:]
      correct_sent = " ".join(correct_word_tokens)
      raw_sent = " ".join(correct_word_tokens_raw)  
      #correct_sent = 
      total_errors += erros_sent
      correcao += " " + correct_sent
      raw += " " + raw_sent
      progress_bar.progress((i+1) / total_sentences)
      progress_bar.progress(progress * (i+1))
   taxa = taxa_acerto(total_errors,total_sentences)
   print("Taxa de acerto: ", taxa)
   return correcao,raw


def on_change():
   st.session_state.changed = True

def on_change_genre():
   st.session_state.changed = True
   st.session_state.action = None

genre = st.radio(
    "Select your input",
    ('Image', 'Text'),horizontal=True, on_change=on_change_genre)


if st.session_state.genre != genre:
   st.session_state.genre = genre
   st.session_state.changed = True


language = 'eng'
text = None
if genre == 'Image':
   uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg"])
   if uploaded_file:
      langs = pytesseract.get_languages()
      eng_index = langs.index('eng')
      st.image(uploaded_file, use_column_width=True)
      language = st.selectbox('Language',langs, index=eng_index)
      text = pytesseract.image_to_string(Image.open(uploaded_file), lang=language)
      size = text.count("\n") * 25
      text = st.text_area("Text",text, on_change=on_change, height=size)
else:
   text = st.text_area("Enter your text",on_change=on_change) 

col1, col2 = st.columns([0.15, 1])

corrected_text = None


if text and language == 'eng':
   if col1.button("Correct") or st.session_state.action == "Correct":
      st.session_state.action = "Correct"
      if st.session_state.changed:
         st.session_state.text,st.session_state.raw = grammar_correct(text)
         st.session_state.changed = False
      st.session_state.out = st.radio("Select your output",('Highlight','Raw'),horizontal=True, key=text)
      if st.session_state.out == 'Highlight':
         print(st.session_state.text)
         st.markdown(st.session_state.text)
      if st.session_state.out == 'Raw':
         size = st.session_state.raw.count("\n") * 25
         st.markdown(st.session_state.raw)

   if col2.button("Summarize") or st.session_state.action == "Summarize":
      st.session_state.action = "Summarize"
      percentage = st.select_slider(
         'Summarized text percentage of Original text (default = 50%)',
         options=[25, 50, 75], value = 50)
      if corrected_text:
         st.write(summarize(corrected_text, percentage))
      elif text: 
         st.write(summarize(text, percentage))


