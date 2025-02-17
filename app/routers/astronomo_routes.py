from fastapi import APIRouter, HTTPException, Query
from models.astronomo import Astronomo

router = APIRouter()

@router.post("/", response_model=dict)
async def create_astronomo(data: dict):
    astronomo = Astronomo(**data)
    astronomo.save()
    return {"message": "Astrônomo criado com sucesso", "data": astronomo.to_mongo().to_dict()}

@router.get("/", response_model=dict)
async def get_all_astronomo(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Astronomo.objects.count()  
    estrelas = Astronomo.objects.skip(skip).limit(limit)  
    data = [estrela.to_mongo().to_dict() for estrela in estrelas]
    return {"quantidade": total, "count": len(data), "estrelas": data}

@router.get("/{astronomo_id}", response_model=dict)
async def get_astronomo_by_id(astronomo_id: str):
    astronomo = Astronomo.objects(id=astronomo_id).first()
    if not astronomo:
        raise HTTPException(status_code=404, detail="Astrônomo não encontrado")
    return astronomo.to_mongo().to_dict()

@router.put("/{astronomo_id}", response_model=dict)
async def update_astronomo(astronomo_id: str, data: dict):
    astronomo = Astronomo.objects(id=astronomo_id).first()
    if not astronomo:
        raise HTTPException(status_code=404, detail="Astrônomo não encontrado")
    astronomo.update(**data)
    astronomo.reload()
    return {"message": "Astrônomo atualizado com sucesso", "data": astronomo.to_mongo().to_dict()}

@router.delete("/{astronomo_id}", response_model=dict)
async def delete_astronomo(astronomo_id: str):
    astronomo = Astronomo.objects(id=astronomo_id).first()
    if not astronomo:
        raise HTTPException(status_code=404, detail="Astrônomo não encontrado")
    astronomo.delete()
    return {"message": "Astrônomo excluído com sucesso"}
