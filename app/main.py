from fastapi import FastAPI, HTTPException
from config.database import db 
from routes import app as routes_app

app = FastAPI()

app.include_router(routes_app)


@app.get("/")
async def root():

    try:
        db.command("ping") 
        return {"message": "Conexão com o MongoDB bem-sucedida!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar no MongoDB: {e}")