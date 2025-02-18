from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models.observacao import Observacao
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    
    if "estrela" in doc and isinstance(doc["estrela"], ObjectId):
        doc["estrela"] = str(doc["estrela"])
    
    if "planetas" in doc and isinstance(doc["planetas"], ObjectId):
        doc["planetas"] = str(doc["planetas"])
    
    return doc

@router.get("/", response_model=dict)
async def get_all_observacoes(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Observacao.objects.count()  
    observacoes = Observacao.objects.skip(skip).limit(limit)  
    data = [convert_objectid(obs.to_mongo().to_dict()) for obs in observacoes]

    return {"quantidade": total, "count": len(data), "observacoes": data}

@router.get("/{observacao_id}", response_model=dict)
async def get_observacao_by_id(observacao_id: str):
    if not ObjectId.is_valid(observacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    
    return convert_objectid(observacao.to_mongo().to_dict())

@router.post("/", response_model=dict)
async def create_observacao(data: dict):
    try:
        if "datahora" in data and isinstance(data["datahora"], str):
            try:
                data["datahora"] = datetime.fromisoformat(data["datahora"])
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")

        for key in ["telescopio", "astronomo"]:
            if key in data and isinstance(data[key], str):
                if not ObjectId.is_valid(data[key]):
                    raise HTTPException(status_code=400, detail=f"ID inválido para {key}.")
                data[key] = ObjectId(data[key])

        if "fenomenos" in data and isinstance(data["fenomenos"], list):
            data["fenomenos"] = [ObjectId(f) if ObjectId.is_valid(f) else HTTPException(status_code=400, detail="ID de fenômeno inválido.") for f in data["fenomenos"]]
        
        observacao = Observacao(**data)
        observacao.save()
        return {"message": "Observação criada com sucesso", "data": convert_objectid(observacao.to_mongo().to_dict())}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{observacao_id}", response_model=dict)
async def update_observacao(observacao_id: str, data: dict):
    if not ObjectId.is_valid(observacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    
    for key in ["telescopio", "astronomo"]:
        if key in data and isinstance(data[key], str):
            if not ObjectId.is_valid(data[key]):
                raise HTTPException(status_code=400, detail=f"ID inválido para {key}.")
            data[key] = ObjectId(data[key])
    
    if "fenomenos" in data and isinstance(data["fenomenos"], list):
        data["fenomenos"] = [ObjectId(f) if ObjectId.is_valid(f) else HTTPException(status_code=400, detail="ID de fenômeno inválido.") for f in data["fenomenos"]]
    
    observacao.update(**data)
    observacao.reload()
    return {"message": "Observação atualizada com sucesso", "data": convert_objectid(observacao.to_mongo().to_dict())}

@router.delete("/{observacao_id}", response_model=dict)
async def delete_observacao(observacao_id: str):
    if not ObjectId.is_valid(observacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    
    observacao.delete()
    return {"message": "Observação excluída com sucesso"}
