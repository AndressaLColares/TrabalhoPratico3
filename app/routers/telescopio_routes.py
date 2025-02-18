from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models.telescopio import Telescopio
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    """Converte ObjectId para string em um dicionário do MongoDB."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=dict)
async def create_telescopio(data: dict):
    try:
        if "data_lancamento" in data and isinstance(data["data_lancamento"], str):
            try:
                data["data_lancamento"] = datetime.fromisoformat(data["data_lancamento"])
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")
        telescopio = Telescopio(**data)
        telescopio.save()
        return {"message": "Telescópio criado com sucesso", "data": convert_objectid(telescopio.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=dict)
async def get_all_telescopios(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Telescopio.objects.count()  # Contagem total de registros
    telescopios = Telescopio.objects.skip(skip).limit(limit)  # Paginação
    data = [convert_objectid(telescopio.to_mongo().to_dict()) for telescopio in telescopios]
    return {"total": total, "count": len(data), "telescopios": data}

@router.get("/{telescopio_id}", response_model=dict)
async def get_telescopio_by_id(telescopio_id: str):
    if not ObjectId.is_valid(telescopio_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    telescopio = Telescopio.objects(id=telescopio_id).first()
    if not telescopio:
        raise HTTPException(status_code=404, detail="Telescópio não encontrado")

    return {"data": convert_objectid(telescopio.to_mongo().to_dict())}

@router.put("/{telescopio_id}", response_model=dict)
async def update_telescopio(telescopio_id: str, data: dict):
    if not ObjectId.is_valid(telescopio_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    telescopio = Telescopio.objects(id=telescopio_id).first()
    if not telescopio:
        raise HTTPException(status_code=404, detail="Telescópio não encontrado")

    telescopio.update(**data)
    telescopio.reload()
    return {"message": "Telescópio atualizado com sucesso", "data": convert_objectid(telescopio.to_mongo().to_dict())}

@router.delete("/{telescopio_id}", response_model=dict)
async def delete_telescopio(telescopio_id: str):
    if not ObjectId.is_valid(telescopio_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    telescopio = Telescopio.objects(id=telescopio_id).first()
    if not telescopio:
        raise HTTPException(status_code=404, detail="Telescópio não encontrado")

    telescopio.delete()
    return {"message": "Telescópio deletado com sucesso"}
