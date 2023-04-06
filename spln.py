import streamlit as st
import pandas as pd
import pytesseract
from io import StringIO
from PIL import Image


# If you don't have tesseract executable in your PATH, include the following:
#pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string

from gramformer import Gramformer
from nltk.tokenize import sent_tokenize


def grammar_correct(influent_sentence):
   gf = Gramformer(models = 1, use_gpu=False) # 1=corrector, 2=detector
    # "the collection of letters was original used by the ancient Romans",
    # "We enjoys horror movies",
    # "Anna and Mike is going skiing",
    # "I walk to the store and I bought milk",
    # " We all eat the fish and then made dessert",
    # "I will eat fish for dinner and drink milk",
    # "what be the reason for everyone leave the company",
    # "He is a really sympathetic person.",
   
   sentences = sent_tokenize(influent_sentence)
   print("[Input] => ", influent_sentence)
   total_sentences = len(sentences)
   total_errors = 0
   correcao = """"""
   print(sentences)
   for i, sent in enumerate(sentences):
       corrected_sentences = gf.correct(sent, max_candidates=1)
       print(corrected_sentences)
       for corrected_sentence in corrected_sentences:
           if corrected_sentence != sent:
               total_errors += 1
           correcao += corrected_sentence
           print("[Edits] ", gf.get_edits(sent, corrected_sentence))
           print("[Edits] ", gf.highlight(sent, corrected_sentence))
   print("-" *100)
   print("[Correção] => ",correcao)
   print("-" *100)

   ser = total_errors / total_sentences
   percent_correct = (1 - ser) * 100
   print(f"Taxa de Acerto = {percent_correct}")
   print("-" *100)
   return correcao


genre = st.radio(
    "Select your input",
    ('Image', 'Text'),horizontal=True)

text = None
if genre == 'Image':
   uploaded_files = st.file_uploader("Choose a file",accept_multiple_files=True)
   for uploaded_file in uploaded_files:
      st.image(uploaded_file, use_column_width=True)
      text = pytesseract.image_to_string(Image.open(uploaded_file))
      st.write(text)
else:
   text = st.text_area("Enter your text")

import pyperclip

if text:
   if st.button("Correct"):
      st.write(grammar_correct(text))
