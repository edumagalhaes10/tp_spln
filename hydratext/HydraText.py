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
### 📸 Extract text from images

### 📄 Extract text from PDFs

### 📄 Correct grammar

### 📄 Summarize text

### 📊 Analyze text sentiment

### 📊 Text statistics

""")

#st.sidebar.success("Select a demo above.")

# extract table from html








