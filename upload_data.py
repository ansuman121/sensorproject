from pymongo.mongo_client import MongoClient
import pandas as pd
import json
"""import logging
logging.basicConfig(level=logging.DEBUG)"""

uri = "mongodb+srv://ansuman121:12345@cluster0.q8loj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

database_name = "ansuman121"
collection_name = "waferfault"

df = pd.read_csv("/Users/ansumanpattanaik/Desktop/sensorproject/notebook/wafer_23012020_041211.csv")
df = df.drop("Unnamed: 0",axis= 1)

json_record = list(json.loads(df.T.to_json()).values())
print(type(json_record))
client[database_name][collection_name].insert_many(json_record)
