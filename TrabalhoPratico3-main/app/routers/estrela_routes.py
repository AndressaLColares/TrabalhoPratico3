from fastapi import APIRouter, HTTPException, Query
from models.estrela import Estrela
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=dict)
async def create_estrela(data: dict):
    try:
        estrela = Estrela(**data)
        estrela.save()
        return {"message": "Estrela criada com sucesso", "data": convert_objectid(estrela.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Gets
@router.get("/", response_model=dict)
async def get_all_estrelas(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Estrela.objects.count()
    estrelas = Estrela.objects.skip(skip).limit(limit)
    data = [convert_objectid(estrela.to_mongo().to_dict()) for estrela in estrelas]
    return {"total": total, "count": len(data), "estrelas": data}

@router.get("/{estrela_id}", response_model=dict)
async def get_estrela_by_id(estrela_id: str):
    if not ObjectId.is_valid(estrela_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    estrela = Estrela.objects(id=estrela_id).first()
    if not estrela:
        raise HTTPException(status_code=404, detail="Estrela não encontrada")

    return {"data": convert_objectid(estrela.to_mongo().to_dict())}

@router.get("/{estrela_id}/filtrar", response_model=dict)
async def get_estrelas_by(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    nome: str = Query(None, description="Filtrar por nome"),
    tipo_espectral: str = Query(None, description="Filtrar por tipo espectral"),
    magnitude_min: float = Query(None, description="Filtrar por magnitude (mínimo)"),
    magnitude_max: float = Query(None, description="Filtrar por magnitude (máximo)"),
    ordenacao: str = Query(None, description="Ordenar por campo (ex: nome, magnitude)"),
    ordem_ascendente: bool = Query(True, description="Ordem ascendente (True) ou descendente (False)"),
):
    query = {}
    if nome:
        query["nome"] = {"$regex": nome, "$options": "i"}  # Busca por texto parcial (case-insensitive)
    if tipo_espectral:
        query["tipo_espectral"] = {"$regex": tipo_espectral, "$options": "i"}
    if magnitude_min is not None:
        query["magnitude__gte"] = magnitude_min  # Maior ou igual que
    if magnitude_max is not None:
        query["magnitude__lte"] = magnitude_max  # Menor ou igual que

    total = Estrela.objects(**query).count()

    # Ordenação
    if ordenacao:
        sinal = "" if ordem_ascendente else "-"  # "-" para ordem descendente
        estrelas = Estrela.objects(**query).order_by(sinal + ordenacao).skip(skip).limit(limit)
    else:  # Ordenação padrão (se nenhum campo for especificado)
      estrelas = Estrela.objects(**query).skip(skip).limit(limit)


    data = [convert_objectid(estrela.to_mongo().to_dict()) for estrela in estrelas]
    return {"total": total, "count": len(data), "estrelas": data}

@router.get("/{estrela_id}/planetas", response_model=dict)
async def get_planetas_by_estrela(estrela_id: str):
    if not ObjectId.is_valid(estrela_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    planetas = Planeta.objects(estrela=estrela_id)
    data = [convert_objectid(planeta.to_mongo().to_dict()) for planeta in planetas]
    return {"count": len(data), "planetas": data}

@router.get("/{estrela_id}/exoplanetas", response_model=dict)
async def get_exoplanetas_by_estrela(estrela_id: str):
    if not ObjectId.is_valid(estrela_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    exoplanetas = Exoplaneta.objects(estrela=estrela_id)
    data = [convert_objectid(exoplaneta.to_mongo().to_dict()) for exoplaneta in exoplanetas]
    return {"count": len(data), "exoplanetas": data}

@router.get("/{estrela_id}/consulta_planeta", response_model=dict)
async def get_in_planeta(tipo_planeta: str = Query(None, description="Tipo de planeta")):
    estrelas = Estrela.objects(planetas__tipo=tipo_planeta)
    data = [convert_objectid(estrela.to_mongo().to_dict()) for estrela in estrelas]
    return {"count": len(data), "estrelas": data}

@router.get("/{estrela_id}/consulta_exoplaneta", response_model=dict)
async def get_in_exoplaneta(nome_exoplaneta: str = Query(None, description="Nome do exoplaneta")):
    estrelas = Estrela.objects(exoplanetas__nome=nome_exoplaneta)
    data = [convert_objectid(estrela.to_mongo().to_dict()) for estrela in estrelas]
    return {"count": len(data), "estrelas": data}

@router.put("/{estrela_id}", response_model=dict)
async def update_estrela(estrela_id: str, data: dict):
    if not ObjectId.is_valid(estrela_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    estrela = Estrela.objects(id=estrela_id).first()
    if not estrela:
        raise HTTPException(status_code=404, detail="Estrela não encontrada")

    estrela.update(**data)
    estrela.reload()
    return {"message": "Estrela atualizada com sucesso", "data": convert_objectid(estrela.to_mongo().to_dict())}

@router.delete("/{estrela_id}", response_model=dict)
async def delete_estrela(estrela_id: str):
    if not ObjectId.is_valid(estrela_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    estrela = Estrela.objects(id=estrela_id).first()
    if not estrela:
        raise HTTPException(status_code=404, detail="Estrela não encontrada")

    estrela.delete()
    return {"message": "Estrela deletada com sucesso"}
