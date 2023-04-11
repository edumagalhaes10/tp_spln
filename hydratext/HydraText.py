import streamlit as st

from PIL import Image
import os
folder = os.path.dirname(os.path.abspath(__file__))

icon = Image.open(f'{folder}/images/favicon.png')
st.set_page_config(
    page_title="HydraText",
    page_icon=icon,
)

image = Image.open(f'{folder}/images/hydratext_title.png')
st.image(image,width=400)


st.markdown("""
## Welcome to HydraText, 
A Natural Language Processing tool developed in the context of a Software Engineering Master's course: Scripting in Natural Language Proccesing. 

The present tool provides the following functionalities and was designed to be accesible for any person with or without knowledge either in Software Engineering and Natural Language Processing. 

Have fun using our tool!!! We hope it's useful!!! 😁

### 📸 Extract text from images

### 📄 Extract text from PDFs

### 📄 Correct grammar

### 📄 Summarize text

### 📊 Analyze text sentiment

### 📊 Text statistics

""")

#st.sidebar.success("Select a demo above.")

# extract table from html








