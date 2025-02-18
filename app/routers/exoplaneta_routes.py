
from fastapi import APIRouter, HTTPException, Query
from models.exoplaneta import Exoplaneta
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    
    if "estrela" in doc and isinstance(doc["estrela"], ObjectId):
        doc["estrela"] = str(doc["estrela"])
    
    if "planetas" in doc and isinstance(doc["planetas"], list):
        doc["planetas"] = [str(p) if isinstance(p, ObjectId) else p for p in doc["planetas"]]
    
    return doc

@router.post("/", response_model=dict)
async def create_exoplaneta(data: dict):
    
    try:
        if "estrela" in data and isinstance(data["estrela"], str):
            if not ObjectId.is_valid(data["estrela"]):
                raise HTTPException(status_code=400, detail="ID da estrela inválido.")
            data["estrela"] = ObjectId(data["estrela"])
        
        if "planetas" in data and isinstance(data["planetas"], list):
            data["planetas"] = [ObjectId(p) if ObjectId.is_valid(p) else None for p in data["planetas"]]
            if None in data["planetas"]:
                raise HTTPException(status_code=400, detail="ID de planeta inválido.")
        
        exoplaneta = Exoplaneta(**data)
        exoplaneta.save()
        
        response_data = convert_objectid(exoplaneta.to_mongo().to_dict())
        return {"message": "Exoplaneta criado com sucesso", "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=dict)
async def get_all_exoplanetas(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
   
    try:
        total = Exoplaneta.objects.count()
        exoplanetas = Exoplaneta.objects.skip(skip).limit(limit)
        data = [convert_objectid(exoplaneta.to_mongo().to_dict()) for exoplaneta in exoplanetas]
        return {"total": total, "count": len(data), "exoplanetas": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{exoplaneta_id}", response_model=dict)
async def get_exoplaneta_by_id(exoplaneta_id: str):
    
    try:
        if not ObjectId.is_valid(exoplaneta_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        exoplaneta = Exoplaneta.objects(id=exoplaneta_id).first()
        if not exoplaneta:
            raise HTTPException(status_code=404, detail="Exoplaneta não encontrado")

        return {"data": convert_objectid(exoplaneta.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{exoplaneta_id}", response_model=dict)
async def update_exoplaneta(exoplaneta_id: str, data: dict):
   
    try:
        if not ObjectId.is_valid(exoplaneta_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        exoplaneta = Exoplaneta.objects(id=exoplaneta_id).first()
        if not exoplaneta:
            raise HTTPException(status_code=404, detail="Exoplaneta não encontrado")

        # Atualiza os campos fornecidos
        exoplaneta.update(**data)
        exoplaneta.reload()
        return {"message": "Exoplaneta atualizado com sucesso", "data": convert_objectid(exoplaneta.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{exoplaneta_id}", response_model=dict)
async def delete_exoplaneta(exoplaneta_id: str):
   
    try:
        if not ObjectId.is_valid(exoplaneta_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        exoplaneta = Exoplaneta.objects(id=exoplaneta_id).first()
        if not exoplaneta:
            raise HTTPException(status_code=404, detail="Exoplaneta não encontrado")

        exoplaneta.delete()
        return {"message": "Exoplaneta deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))