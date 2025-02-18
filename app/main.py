from fastapi import FastAPI, HTTPException
import config.database 
from routes import app as routes_app

app = FastAPI()

app.include_router(routes_app)

@app.get("/")
async def root():
    try:
        config.database.db.command("ping")
        return {"message": "Conexão com o MongoDB bem-sucedida!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar no MongoDB: {e}")
