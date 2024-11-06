import PyPDF2
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


def parse_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            metadata = {
                "Document Name" : os.path.basename(file_path),
                "Size in kb" : round(os.stat(file_path).st_size / 1024, 2),
                "Time of Ingestion": da

            }

            return [file_path, meta_data, text]
    except Exception as e:
        return file_path, str(e)


def list_of_file(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files


def extract_text_from_folder(folder_path):
    pdf_files = list_of_file(folder_path)
    with ThreadPoolExecutor() as executor:

        # results = list(executor.map(parse_pdf, pdf_files))
        pdf_texts = [parse_pdf(file_path) for file_path in pdf_files]

    return pdf_texts



folder = 'database'
data = extract_text_from_folder(folder)
print(data[0])
# file = 'database/1699521350.pdf'
# print(parse_pdf(file))
