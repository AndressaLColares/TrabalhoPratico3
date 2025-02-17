from fastapi import APIRouter, HTTPException, Query
from models.planeta import Planeta

router = APIRouter()

@router.post("/", response_model=dict)
async def create_planeta(data: dict):
    planeta = Planeta(**data)
    planeta.save()
    return {"message": "Planeta criado com sucesso", "data": planeta.to_mongo().to_dict()}

@router.get("/", response_model=dict)
async def get_all_planetas(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Planeta.objects.count()  # Contagem total de registros
    planetas = Planeta.objects.skip(skip).limit(limit)  # Paginação
    data = [planeta.to_mongo().to_dict() for planeta in planetas]
    return {"total": total, "count": len(data), "planetas": data}

@router.get("/{planeta_id}", response_model=dict)
async def get_planeta_by_id(planeta_id: str):
    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")
    return {"data": planeta.to_mongo().to_dict()}

@router.put("/{planeta_id}", response_model=dict)
async def update_planeta(planeta_id: str, data: dict):
    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")
    planeta.update(**data)
    planeta.reload()
    return {"message": "Planeta atualizado com sucesso", "data": planeta.to_mongo().to_dict()}

@router.delete("/{planeta_id}", response_model=dict)
async def delete_planeta(planeta_id: str):
    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")
    planeta.delete()
    return {"message": "Planeta deletado com sucesso"}
