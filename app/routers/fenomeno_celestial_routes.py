from fastapi import APIRouter, HTTPException, Query
from models.fenomeno_celestial import FenomenoCelestial

router = APIRouter()

@router.post("/", response_model=dict)
async def create_fenomeno_celestial(data: dict):
    fenomeno = FenomenoCelestial(**data)
    fenomeno.save()
    return {"message": "Fenômeno celestial criado com sucesso", "data": fenomeno.to_mongo().to_dict()}

@router.get("/", response_model=dict)
async def get_all_fenomenos_celestiais(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = FenomenoCelestial.objects.count()  # Contagem total de registros
    fenomenos = FenomenoCelestial.objects.skip(skip).limit(limit)  # Paginação
    data = [fenomeno.to_mongo().to_dict() for fenomeno in fenomenos]
    return {"total": total, "count": len(data), "fenomenos_celestiais": data}

@router.get("/{fenomeno_id}", response_model=dict)
async def get_fenomeno_celestial_by_id(fenomeno_id: str):
    fenomeno = FenomenoCelestial.objects(id=fenomeno_id).first()
    if not fenomeno:
        raise HTTPException(status_code=404, detail="Fenômeno celestial não encontrado")
    return {"data": fenomeno.to_mongo().to_dict()}

@router.put("/{fenomeno_id}", response_model=dict)
async def update_fenomeno_celestial(fenomeno_id: str, data: dict):
    fenomeno = FenomenoCelestial.objects(id=fenomeno_id).first()
    if not fenomeno:
        raise HTTPException(status_code=404, detail="Fenômeno celestial não encontrado")
    fenomeno.update(**data)
    fenomeno.reload()
    return {"message": "Fenômeno celestial atualizado com sucesso", "data": fenomeno.to_mongo().to_dict()}

@router.delete("/{fenomeno_id}", response_model=dict)
async def delete_fenomeno_celestial(fenomeno_id: str):
    fenomeno = FenomenoCelestial.objects(id=fenomeno_id).first()
    if not fenomeno:
        raise HTTPException(status_code=404, detail="Fenômeno celestial não encontrado")
    fenomeno.delete()
    return {"message": "Fenômeno celestial deletado com sucesso"}
