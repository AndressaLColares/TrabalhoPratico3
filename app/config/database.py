from pymongo import MongoClient
import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

print("Conectando ao MongoDB...")
print("MONGO_URI:", MONGO_URI)
print("DB_NAME:", DB_NAME)

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  
    client.server_info()  
    print("✅ Conexão bem-sucedida com pymongo!")
    
    connect(DB_NAME, host=MONGO_URI) 
    
    print("✅ Conexão bem-sucedida com mongoengine!")
except Exception as e:
    print("❌ Erro ao conectar no MongoDB:", e)

db = client[DB_NAME]  