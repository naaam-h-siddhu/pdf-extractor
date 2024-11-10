import asyncio
import fitz
import os
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor
import re
from nltk.corpus import stopwords, words
from pymongo import MongoClient

english_words = set(words.words())
stop_words = set(stopwords.words('english'))


def parse_pdf(file_path):
    try:
        with fitz.open(file_path) as file:
            text = ""
            for page_num in range(file.page_count):
                page = file.load_page(page_num)

                text += page.get_text()
            metadata = [
                os.path.basename(file_path),
                round(os.stat(file_path).st_size / 1024, 2),
                datetime.now().isoformat()
            ]

            return [metadata, text]
    except Exception as e:
        return {"error": str(e), "file": file_path}


def list_of_file(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def text_cleaner(content):
    cleaned_content = re.sub(r'\s([,.?!:;])', r'\1', content)  # removes extra space around punctuation
    cleaned_content = re.sub(r'/+', '/', cleaned_content)  # removes extra ////
    cleaned_content = re.sub(r'\.{2,}', '.', cleaned_content)  # removes extra ...
    cleaned_content = re.sub(r'_+', '_', cleaned_content)  # removes extra ___
    cleaned_content = cleaned_content.replace("\n", " ")  # removes /n/n
    cleaned_content = re.sub(r'[\{\}\[\]]', '', cleaned_content)   # Remove any curly braces or square brackets
    cleaned_text = re.sub(r'[^A-Za-z\s]', '', cleaned_content)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)  # Remove non-ASCII characters

    cleaned_text = cleaned_text.lower()
    cleaned_text = cleaned_text.split()
    ans = []
    for word in cleaned_text:
        if len(word) != 1:
            if word in english_words and word not in stop_words:
                ans.append(word)
    cleaned_content = ' '.join(ans)
    return cleaned_content


def convert_to_json(normal_data):
    all_data = []
    for i in range(len(normal_data)):
        temp_data = {
            "data": {
                "Document Name": normal_data[i][0][0],
                "Size(in KB)": normal_data[i][0][1],
                "Time of Ingestion": normal_data[i][0][2],
                "Text": text_cleaner(normal_data[i][1])

            }
        }
        all_data.append(temp_data)
    return all_data


async def extract_text_from_folder(folder_path):
    pdf_files = list_of_file(folder_path)

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=4) as executor:
        start_time = time.time()

        results = await asyncio.gather(
            *[loop.run_in_executor(executor, parse_pdf, file_path) for file_path in pdf_files]
        )

        print(f"Processing Time: {time.time() - start_time} seconds")
    return convert_to_json(results)


def parser(folder):
    json_data = asyncio.run(extract_text_from_folder(folder))
    mongo_url = "mongodb://localhost:27017/"
    database_name = "ingestionDB"
    collections_name = "contentEntries"
    client = MongoClient(mongo_url)
    db = client[database_name]
    collection = db[collections_name]
    # inserting one by one for checking if any pdf have issue
    for doc in json_data:
        pdf_name = doc['data']["Document Name"]
        try:
            collection.insert_one(doc)
            print(f"Successfully inserted document:{pdf_name}")
        except Exception as e:
            print(f"Document  {pdf_name} not uploaded")
    pass



