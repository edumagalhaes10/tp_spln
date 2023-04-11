import streamlit as st
import pytesseract
from PIL import Image
from summarize_text import summarize
from correct import grammar_correct
from gramformer import Gramformer
from nltk.tokenize import sent_tokenize
import nltk
import pdftotext
from PIL import UnidentifiedImageError
from sentiment_analysis import sentiment_analysis
from stats import stats
import wget
import bs4 as bs
import urllib.request
import os
from os.path import expanduser



if 'out' not in st.session_state:
   st.session_state.out = None

if 'changed' not in st.session_state:
   st.session_state.changed = True

if 'input_type' not in st.session_state:
   st.session_state.input_type = None

if 'correct' not in st.session_state:
   st.session_state.correct = None

if 'lang_tesseract' not in st.session_state:
   st.session_state.lang_tesseract = None
   st.session_state.langs = None

if 'nltk_load' not in st.session_state:
   st.session_state.nltk_load = False

if 'tesseract_load' not in st.session_state:
   st.session_state.tesseract_load = False

if st.session_state.nltk_load == False:
   nltk.download('wordnet')
   nltk.download('vader_lexicon') 
   nltk.download('stopwords')
   #nltk.download('punkt')

   st.session_state.nltk_load = True



def on_change():
   st.session_state.changed = True
   st.session_state.correct = None

def on_change_genre():
   st.session_state.changed = True

st.set_page_config(page_title="SPLN", page_icon="📖")

genre = st.radio(
    "Select your input",
    ('Image', 'Text', 'PDF'),horizontal=True, on_change=on_change_genre, index=1)


if st.session_state.input_type != genre:
   st.session_state.input_type = genre
   st.session_state.changed = True


home = expanduser("~/.local/share/tessdata")
os.environ['TESSDATA_PREFIX']= home

if not st.session_state.lang_tesseract:
   sauce = urllib.request.urlopen('https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html').read()
   soup = bs.BeautifulSoup(sauce,'lxml')
   table = soup.find('table')
   table_rows = table.find_all('tr')
   st.session_state.lang_tesseract = {}
   for tr in table_rows:
       td = tr.find_all('td')
       if td:
           st.session_state.lang_tesseract[td[0].text] = td[1].text


   



def install_default():
   if not os.path.exists(home):
      os.makedirs(home)
   elif not os.path.isdir(home):
      st.error(f"{home} is not a directory. Remove it and try again.")
      exit()
   if not os.path.exists(f"{home}/eng.traineddata") and 'eng' not in st.session_state.langs:
      print(st.session_state.langs)
      url = f"https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata"
      output_directory = f"{home}"
      st.session_state.langs.append('eng')
      with st.spinner("Downloading default language..."):
         wget.download(url, out=output_directory)


language = 'eng'
text = None
if genre == 'Image':
   try:
      st.session_state.langs = pytesseract.get_languages()
   except:
      st.error("Tesseract not found. Make sure you have installed. See [installation instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html)")
      exit()
   if not st.session_state.tesseract_load:
      install_default()
      st.session_state.tesseract_load = True
   download = {}
   for lang in st.session_state.lang_tesseract:
      if lang not in st.session_state.langs:
         download[lang] = lang
   download = [f"{lang}: {st.session_state.lang_tesseract[lang]}" if lang in st.session_state.lang_tesseract else f"{lang}: {lang}" for lang in download]
   download[0] = ""
   multi = st.selectbox("Download languages", download,index=0)
   multi = multi.split(":")[0]
   if multi.strip():
      if st.button("Download"):
         with st.spinner("Downloading language..."):
            url = f"https://github.com/tesseract-ocr/tessdata/raw/main/{multi}.traineddata"
            output_directory = f"{home}"
            filename = wget.download(url, out=output_directory)
            st.session_state.langs.append(multi)
   uploaded_file = st.file_uploader("Choose a file")
   if uploaded_file:
      langs = st.session_state.langs
      eng_index = langs.index('eng')
      try:
         st.image(uploaded_file, use_column_width=True)
         langs = [f"{lang}: {st.session_state.lang_tesseract[lang]}" if lang in st.session_state.lang_tesseract else f"{lang}: {lang}" for lang in langs ]
         language = st.selectbox('Language',langs, index=eng_index)
         language = language.split(":")[0]
         text = pytesseract.image_to_string(Image.open(uploaded_file), lang=language)
      except UnidentifiedImageError:
         st.error("Error on image conversion. Make sure the file is an image.")
         exit()
      except:
         st.error("Tesseract not found. Make sure you have installed. See [installation instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html)")
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


if text:
   with col1:
      if language == 'eng':
         if st.button("Start correction!") or st.session_state.correct:
            with st.spinner("Loading grammar model..."):
               if 'gramformer' not in st.session_state:
                  st.session_state.gramformer = Gramformer(models = 1, use_gpu=False)
            st.session_state.correct = True
            if st.session_state.changed:
               st.write("Checking grammar...")
               progress_bar = st.progress(0)
               st.session_state.text,st.session_state.raw = grammar_correct(text,progress_bar,st.session_state.gramformer)
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
      else:
         st.warning("""Only English is supported for grammar correction.""")
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
         st.warning(f"Help: Text must be over {size_text} characters to summarize.")
   with col3:
      language_nltk = st.multiselect('Language of text',langs_nltk,max_selections=1, key="Sent_analysis")
      if language_nltk:
         with st.spinner('Sentiment Analysis...'):
            st.markdown(sentiment_analysis(text, language_nltk))
   with col4:
      language_nltk = st.multiselect('Language of text',langs_nltk,max_selections=1, key="Stats")
      if language_nltk:
         with st.spinner('Calculating Stats...'):   
            st.markdown(stats(text, language_nltk))


