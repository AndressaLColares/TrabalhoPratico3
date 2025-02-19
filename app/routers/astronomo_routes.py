from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models.astronomo import Astronomo
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=dict)
async def create_astronomo(data: dict):
    try:
        if "data_nascimento" in data and isinstance(data["data_nascimento"], str):
            try:
                data["data_nascimento"] = datetime.fromisoformat(data["data_nascimento"])
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")

        astronomo = Astronomo(**data)
        astronomo.save()

        astronomo_dict = convert_objectid(astronomo.to_mongo().to_dict())

        return {"message": "Astrônomo criado com sucesso", "data": astronomo_dict}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=dict)
async def get_all_astronomo(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Astronomo.objects.count()  
    astronomos = Astronomo.objects.skip(skip).limit(limit)  
    data = [convert_objectid(astronomo.to_mongo().to_dict()) for astronomo in astronomos]
    return {"quantidade": total, "count": len(data), "astronomos": data}

@router.get("/{astronomo_id}", response_model=dict)
async def get_astronomo_by_id(astronomo_id: str):
    if not ObjectId.is_valid(astronomo_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    astronomo = Astronomo.objects(id=astronomo_id).first()
    if not astronomo:
        raise HTTPException(status_code=404, detail="Astrônomo não encontrado")
    
    return convert_objectid(astronomo.to_mongo().to_dict())

@router.get("/filtrar/{astronomo_id}", response_model=dict)
async def get_astronomo_by(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    nome: str = Query(None, description="Filtrar por nome"),
    area_estudo: str = Query(None, description="Filtrar por área de estudo"),
    ordenacao: str = Query(None, description="Ordenar por campo (ex: nome, area_estudo)"),
    ordem_ascendente: bool = Query(True, description="Ordem ascendente (True) ou descendente (False)"),
):
    query = {}
    if nome:
        query["nome"] = {"$regex": nome, "$options": "i"}  # Busca por texto parcial (case-insensitive)
    if area_estudo:
        query["area_estudo"] = {"$regex": area_estudo, "$options": "i"}

    total = Astronomo.objects(**query).count()

    # Ordenação
    if ordenacao:
        sinal = "" if ordem_ascendente else "-" 
        astronomos = Astronomo.objects(**query).order_by(sinal + ordenacao).skip(skip).limit(limit)
    else:  
        astronomos = Astronomo.objects(**query).skip(skip).limit(limit)

    data = [convert_objectid(astronomo.to_mongo().to_dict()) for astronomo in astronomos]
    return {"quantidade": total, "count": len(data), "astronomos": data}
@router.get("/{astronomo_id}/observacoes", response_model=dict)
async def get_observacoes_by_astronomo(astronomo_id: str):
    if not ObjectId.is_valid(astronomo_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    observacoes = Observacao.objects(astronomo=astronomo_id)
    data = [convert_objectid(observacao.to_mongo().to_dict()) for observacao in observacoes]
    return {"count": len(data), "observacoes": data}

    
@router.get("{astronomo_id}/consulta_observacao", response_model=dict)
async def get_in_observacao(content: str):

    astronomos = Astronomo.objects(observacoes__propriedades_observadas__icontains=content)

    data = [convert_objectid(astronomo.to_mongo().to_dict()) for astronomo in astronomos]
    return {"count": len(data), "astronomos": data}


@router.put("/{astronomo_id}", response_model=dict)
async def update_astronomo(astronomo_id: str, data: dict):
    if not ObjectId.is_valid(astronomo_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    astronomo = Astronomo.objects(id=astronomo_id).first()
    if not astronomo:
        raise HTTPException(status_code=404, detail="Astrônomo não encontrado")
    
    astronomo.update(**data)
    astronomo.reload()
    return {"message": "Astrônomo atualizado com sucesso", "data": convert_objectid(astronomo.to_mongo().to_dict())}

@router.delete("/{astronomo_id}", response_model=dict)
async def delete_astronomo(astronomo_id: str):
    if not ObjectId.is_valid(astronomo_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    astronomo = Astronomo.objects(id=astronomo_id).first()
    if not astronomo:
        raise HTTPException(status_code=404, detail="Astrônomo não encontrado")
    
    astronomo.delete()
    return {"message": "Astrônomo excluído com sucesso"}
