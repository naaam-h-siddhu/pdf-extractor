
# PDF EXTRACTOR

This project extracts text from PDF documents, identifies key terms, and generates concise summaries, storing all results in a MongoDB database for easy access and retrieval. Built with Python, it leverages Fitz for PDF text extraction, Natural Language Processing (NLP) for keyword and summary generation, and MongoDB for structured data storage.



## Features


- Extracts and processes text from PDF files
- Identifies important keywords and key phrases
- Generates concise summaries of PDF content
- Saves extracted keywords and summaries to MongoDB
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/naaam-h-siddhu/pdf-extractor.git
```

Go to the project directory

```bash
  cd pdf-extractor
```

### Install dependencies

```bash
  pip install pymongo
  pip install pymupdf
  pip install transformers
  pip install language-tool-python
  pip install nltk
  pip install asyncio
  pip install torch
```


Additionally, for nltk stopwords and tokenization features, you need to download some NLTK data:


```
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')
```
