from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models.planeta import Planeta
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    """Converte ObjectId para string em um dicionário do MongoDB."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=dict)
async def create_planeta(data: dict):
    try:
        if "data_descoberta" in data and isinstance(data["data_descoberta"], str):
            try:
                data["data_descoberta"] = datetime.fromisoformat(data["data_descoberta"])
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")
    
        planeta = Planeta(**data)
        planeta.save()
        return {"message": "Planeta criado com sucesso", "data": convert_objectid(planeta.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=dict)
async def get_all_planetas(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Planeta.objects.count()  # Contagem total de registros
    planetas = Planeta.objects.skip(skip).limit(limit)  # Paginação
    data = [convert_objectid(planeta.to_mongo().to_dict()) for planeta in planetas]
    return {"total": total, "count": len(data), "planetas": data}

@router.get("/{planeta_id}", response_model=dict)
async def get_planeta_by_id(planeta_id: str):
    if not ObjectId.is_valid(planeta_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")

    return {"data": convert_objectid(planeta.to_mongo().to_dict())}

@router.put("/{planeta_id}", response_model=dict)
async def update_planeta(planeta_id: str, data: dict):
    if not ObjectId.is_valid(planeta_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")

    planeta.update(**data)
    planeta.reload()
    return {"message": "Planeta atualizado com sucesso", "data": convert_objectid(planeta.to_mongo().to_dict())}

@router.delete("/{planeta_id}", response_model=dict)
async def delete_planeta(planeta_id: str):
    if not ObjectId.is_valid(planeta_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")

    planeta.delete()
    return {"message": "Planeta deletado com sucesso"}
