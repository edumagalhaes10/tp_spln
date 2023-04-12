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


filename_md = os.path.dirname(folder) + "/hydratext/README.md"

with open(filename_md, "r") as f:
    readme_text = f.readlines()
    readme_text = readme_text[1:]
    readme_text = "".join(readme_text)
    st.markdown(readme_text,unsafe_allow_html=True)

#st.sidebar.success("Select a demo above.")

# extract table from html








