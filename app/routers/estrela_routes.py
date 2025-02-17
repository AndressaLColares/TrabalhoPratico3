
from fastapi import APIRouter, HTTPException, Query
from models.estrela import Estrela

router = APIRouter()

@router.post("/", response_model=dict)
async def create_estrela(data: dict):
    estrela = Estrela(**data)
    estrela.save()
    return {"message": "Estrela criada com sucesso", "data": estrela.to_mongo().to_dict()}

@router.get("/", response_model=dict)
async def get_all_estrelas(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Estrela.objects.count()  # Contagem total de registros
    estrelas = Estrela.objects.skip(skip).limit(limit)  # Paginação
    data = [estrela.to_mongo().to_dict() for estrela in estrelas]
    return {"total": total, "count": len(data), "estrelas": data}

@router.get("/{estrela_id}", response_model=dict)
async def get_estrela_by_id(estrela_id: str):
    estrela = Estrela.objects(id=estrela_id).first()
    if not estrela:
        raise HTTPException(status_code=404, detail="Estrela não encontrada")
    return {"data": estrela.to_mongo().to_dict()}

@router.put("/{estrela_id}", response_model=dict)
async def update_estrela(estrela_id: str, data: dict):
    estrela = Estrela.objects(id=estrela_id).first()
    if not estrela:
        raise HTTPException(status_code=404, detail="Estrela não encontrada")
    estrela.update(**data)
    estrela.reload()
    return {"message": "Estrela atualizada com sucesso", "data": estrela.to_mongo().to_dict()}

@router.delete("/{estrela_id}", response_model=dict)
async def delete_estrela(estrela_id: str):
    estrela = Estrela.objects(id=estrela_id).first()
    if not estrela:
        raise HTTPException(status_code=404, detail="Estrela não encontrada")
    estrela.delete()
    return {"message": "Estrela deletada com sucesso"}
