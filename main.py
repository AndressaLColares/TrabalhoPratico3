from fastapi import FastAPI, HTTPException
from database import db 

app = FastAPI()

@app.get("/")
async def root():

    try:
        db.command("ping") 
        return {"message": "Conexão com o MongoDB bem-sucedida!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar no MongoDB: {e}")