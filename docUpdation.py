from pymongo import MongoClient
from keywords import extract_keyword
from summarization import summary_maker


def update():
    mongo_url = "mongodb://localhost:27017/"
    database_name = "ingestionDB"
    collections_name = "contentEntries"
    client = MongoClient(mongo_url)
    db = client[database_name]
    collection = db[collections_name]
    datas = list(collection.find())
    i = 1
    for data in datas:
        ids = data['_id']

        text = data['data']['Text']

        keywords = extract_keyword(text)
        collection.update_one({"_id": ids}, {"$set": {"keywords": keywords}})
        summary = summary_maker(text)
        collection.update_one({"_id": ids}, {"$set": {"summary": summary}})
        print(f"Document {i} updated with keywords and summary")
        i += 1





