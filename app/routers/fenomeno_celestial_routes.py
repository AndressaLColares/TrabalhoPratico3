from fastapi import APIRouter, HTTPException, Query
from models.fenomeno_celestial import FenomenoCelestial
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=dict)
async def create_fenomeno_celestial(data: dict):
    try:
        fenomeno = FenomenoCelestial(**data)
        fenomeno.save()
        return {"message": "Fenômeno celestial criado com sucesso", "data": convert_objectid(fenomeno.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=dict)
async def get_all_fenomenos_celestiais(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = FenomenoCelestial.objects.count()
    fenomenos = FenomenoCelestial.objects.skip(skip).limit(limit)
    data = [convert_objectid(fenomeno.to_mongo().to_dict()) for fenomeno in fenomenos]
    return {"total": total, "count": len(data), "fenomenos_celestiais": data}

@router.get("/{fenomeno_id}", response_model=dict)
async def get_fenomeno_celestial_by_id(fenomeno_id: str):
    if not ObjectId.is_valid(fenomeno_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    fenomeno = FenomenoCelestial.objects(id=fenomeno_id).first()
    if not fenomeno:
        raise HTTPException(status_code=404, detail="Fenômeno celestial não encontrado")

    return {"data": convert_objectid(fenomeno.to_mongo().to_dict())}

@router.put("/{fenomeno_id}", response_model=dict)
async def update_fenomeno_celestial(fenomeno_id: str, data: dict):
    if not ObjectId.is_valid(fenomeno_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    fenomeno = FenomenoCelestial.objects(id=fenomeno_id).first()
    if not fenomeno:
        raise HTTPException(status_code=404, detail="Fenômeno celestial não encontrado")

    fenomeno.update(**data)
    fenomeno.reload()
    return {"message": "Fenômeno celestial atualizado com sucesso", "data": convert_objectid(fenomeno.to_mongo().to_dict())}

@router.delete("/{fenomeno_id}", response_model=dict)
async def delete_fenomeno_celestial(fenomeno_id: str):
    if not ObjectId.is_valid(fenomeno_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    fenomeno = FenomenoCelestial.objects(id=fenomeno_id).first()
    if not fenomeno:
        raise HTTPException(status_code=404, detail="Fenômeno celestial não encontrado")

    fenomeno.delete()
    return {"message": "Fenômeno celestial deletado com sucesso"}
