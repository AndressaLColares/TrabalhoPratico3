import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

db = client["TrabalhoPratico3"] 

try:
    client.admin.command('ping')
    print("Conexão com MongoDB Atlas feita com sucesso!")
except Exception as e:
    print(f"Erro ao conectar no MongoDB: {e}")
