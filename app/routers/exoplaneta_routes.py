from fastapi import APIRouter, HTTPException, Query
from models.exoplaneta import Exoplaneta

router = APIRouter()

@router.post("/", response_model=dict)
async def create_exoplaneta(data: dict):
    exoplaneta = Exoplaneta(**data)
    exoplaneta.save()
    return {"message": "Exoplaneta criado com sucesso", "data": exoplaneta.to_mongo().to_dict()}

@router.get("/", response_model=dict)
async def get_all_exoplanetas(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Exoplaneta.objects.count()  # Contagem total de registros
    exoplanetas = Exoplaneta.objects.skip(skip).limit(limit)  # Paginação
    data = [exoplaneta.to_mongo().to_dict() for exoplaneta in exoplanetas]
    return {"total": total, "count": len(data), "exoplanetas": data}

@router.get("/{exoplaneta_id}", response_model=dict)
async def get_exoplaneta_by_id(exoplaneta_id: str):
    exoplaneta = Exoplaneta.objects(id=exoplaneta_id).first()
    if not exoplaneta:
        raise HTTPException(status_code=404, detail="Exoplaneta não encontrado")
    return {"data": exoplaneta.to_mongo().to_dict()}

@router.put("/{exoplaneta_id}", response_model=dict)
async def update_exoplaneta(exoplaneta_id: str, data: dict):
    exoplaneta = Exoplaneta.objects(id=exoplaneta_id).first()
    if not exoplaneta:
        raise HTTPException(status_code=404, detail="Exoplaneta não encontrado")
    exoplaneta.update(**data)
    exoplaneta.reload()
    return {"message": "Exoplaneta atualizado com sucesso", "data": exoplaneta.to_mongo().to_dict()}

@router.delete("/{exoplaneta_id}", response_model=dict)
async def delete_exoplaneta(exoplaneta_id: str):
    exoplaneta = Exoplaneta.objects(id=exoplaneta_id).first()
    if not exoplaneta:
        raise HTTPException(status_code=404, detail="Exoplaneta não encontrado")
    exoplaneta.delete()
    return {"message": "Exoplaneta deletado com sucesso"}
