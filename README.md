<img src="hydratext/images/hydratext_title.png">

[![License](https://img.shields.io/npm/l/express?style=flat-square)](https://github.com/edumagalhaes10/tp_spln/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![pytesseract](https://img.shields.io/badge/pytesseract->=0.3.10-blue.svg)](https://shields.io/)
[![gramformer](https://img.shields.io/badge/gramformer->=1.0-blue.svg)](https://shields.io/)
[![nltk](https://img.shields.io/badge/nltk->=3.8.1-blue.svg)](https://shields.io/)
[![streamlit](https://img.shields.io/badge/streamlit->=1.20.0-blue.svg)](https://shields.io/)


## Welcome to HydraText, 
A Natural Language Processing tool developed in the context of a Software Engineering Master's course: Scripting in Natural Language Processing. 

The present tool provides the following functionalities and is designed to be accessible for any person with or without knowledge either in Software Engineering and Natural Language Processing. 

Have fun using our tool!!! We hope it's useful!!! 😁

> **Note:** After installing the tool, the command *hydratxt_post_install* may be run.

### 📸 Extract text from images and PDFs

Provide an image of any type and the text will be extracted from it.
The default language is English, but you can also use other languages.
For that, in the image section just select the language you want to use and download it.

<img src="readme_images/to_recognize.png">

<img src="readme_images/recognized_text.png">

**Note**: This feature uses the Tesseract OCR engine. To use it, you need to download it first. See [installation instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html).

You can also extract text from a PDF file. Just upload it and the text will be extracted.

### 📄 Correct grammar

Provide a text, or use the text extracted from an image or PDF, and the grammar will be corrected.
The corrected text can be seen in two ways:
- **Highlights**: The words that were removed will be highlighted in red and the words that were added will be highlighted in green.

<img src="readme_images/correction_highlight.png">

- **Raw**: The corrected text with no highlights.

<img src="readme_images/correction_raw.png">

### 📄 Summarize text

Provide a text, use the text extracted from an image or PDF, or the text with the grammar corrected. The result will be a summary of the text.
The length of the summary can be changed by the user. Default value is 50% of the original text but it can be changed to 25% or 75% of it.

<img src="readme_images/summarization.png">

### 📊 Analyze text sentiment

Provide a text, or use the text extracted from an image or PDF or the text with the grammar corrected, and it will tell if the text is neutral, postive or negative in what comes to sentiment.

<img src="readme_images/sentiment_analysis.png">

### 📊 Text statistics

Provide a text, or use the text extracted from an image or PDF and it will show the following statistics:

- Vocabulary size (number of unique words)
- Top 10 most used words
- Top 10 most used words without stopwords
- List of collocations (A sequence of words that occurs together unusually often.)