import streamlit as st
import pytesseract
from PIL import Image
from summarize_text import summarize
from correct import correct_sentence, taxa_acerto
from gramformer import Gramformer
from nltk.tokenize import sent_tokenize
import pdftotext
from PIL import UnidentifiedImageError
from sentiment_analysis import sentiment_analysis
from stats import stats


#Session State

if 'gramformer' not in st.session_state:
   st.session_state.gramformer = Gramformer(models = 1, use_gpu=False)

if 'out' not in st.session_state:
   st.session_state.out = None

if 'changed' not in st.session_state:
   st.session_state.changed = True

if 'genre' not in st.session_state:
   st.session_state.genre = None

if 'correct' not in st.session_state:
   st.session_state.correct = None




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
      print(f'CORRECT_SENT : {correct_sent}')

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

st.set_page_config(page_title="SPLN", page_icon="📖")




genre = st.radio(
    "Select your input",
    ('Image', 'Text', 'PDF'),horizontal=True, on_change=on_change_genre)


if st.session_state.genre != genre:
   st.session_state.genre = genre
   st.session_state.changed = True


language = 'eng'
text = None
if genre == 'Image':
   uploaded_file = st.file_uploader("Choose a file")
   if uploaded_file:
      langs = pytesseract.get_languages()
      eng_index = langs.index('eng')
      try:
         st.image(uploaded_file, use_column_width=True)
         language = st.selectbox('Language',langs, index=eng_index)
         text = pytesseract.image_to_string(Image.open(uploaded_file), lang=language)
      except UnidentifiedImageError:
         st.error("Error on image conversion. Make sure the file is an image.")
         exit()
      size = text.count("\n") * 25
      text = st.text_area("Text",text, on_change=on_change, height=size)
elif genre == 'PDF':
    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
    if uploaded_file:
        pdf = pdftotext.PDF(uploaded_file)
        text = "\n\n".join(pdf)
else:
   uploaded_file = st.file_uploader("Choose a file", type=["txt"])
   text = ""
   if uploaded_file:
      text = uploaded_file.read().decode('utf-8')
   text = st.text_area("Enter your text",text,on_change=on_change) 


col1, col2, col3, col4 = st.tabs(["Correct", "Summarize", "Sentiment Analysis", "Stats"])



size_text = 100

langs_nltk = ['arabic', 'azerbaijani', 'basque', 'bengali', 'catalan', 'chinese', 'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'greek', 'hebrew', 'hinglish', 'hungarian', 'indonesian', 'italian', 'kazakh', 'nepali', 'norwegian', 'portuguese', 'romanian', 'russian', 'slovene', 'spanish', 'swedish', 'tajik', 'turkish']


if text and language == 'eng':
   with col1:
      if st.button("Start correction!") or st.session_state.correct:
         st.session_state.correct = True
         if st.session_state.changed:
            st.session_state.text,st.session_state.raw = grammar_correct(text)
            st.session_state.changed = False
         st.session_state.out = st.radio("Select your output",('Highlight','Raw'),horizontal=True, key=text)
         if st.session_state.out == 'Highlight':
            st.markdown(st.session_state.text)
         if st.session_state.out == 'Raw':
            st.session_state.raw = st.text_area("Output Text",st.session_state.raw)
         disabled = not(len(st.session_state.raw) > size_text)
         c1,c2 = st.tabs(["Summarize", "Sentiment Analysis"])
         with c1:
            language_nltk = st.multiselect('Language of text',langs_nltk,key="correct_box",max_selections=1)
            if language_nltk:
               percentage = st.select_slider(
                  'Summarized text percentage of Original text (default = 50%)',
                  options=[25, 50, 75], value = 50, key="Correct")
               with st.spinner('Summarizing...'):
                  st.write(summarize(st.session_state.raw, percentage,language_nltk))
         with c2:
            language_nltk = st.multiselect('Language of text',langs_nltk,max_selections=1,key="sentiment")
            if language_nltk:
               with st.spinner("Sentiment Analysis..."):
                  st.markdown(sentiment_analysis(text, language_nltk))
   disabled = not(len(text) > size_text)
   with col2:
      if not disabled:
         language_nltk = st.multiselect('Language of text',langs_nltk,max_selections=1)
         if language_nltk:
            percentage = st.select_slider(
               'Summarized text percentage of Original text (default = 50%)',
               options=[25, 50, 75], value = 50)
            with st.spinner('Summarizing...'):
               st.write(summarize(text, percentage,language_nltk))
      else:
         st.markdown("Help: Text must be over {size_text} chars")
   with col3:
      language_nltk = st.multiselect('Language of text',langs_nltk,max_selections=1, key="Sent_analysis")
      if language_nltk:
         with st.spinner('Sentiment Analysis...'):
            st.markdown(sentiment_analysis(text, language_nltk))
   with col4:
      with st.spinner('Calculating Stats...'):   
            st.markdown(stats(text))


