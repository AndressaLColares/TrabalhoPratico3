from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models.telescopio import Telescopio
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    """Converte ObjectId para string em um dicionário do MongoDB."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=dict)
async def create_telescopio(data: dict):
    try:
        if "data_lancamento" in data and isinstance(data["data_lancamento"], str):
            try:
                data["data_lancamento"] = datetime.fromisoformat(data["data_lancamento"])
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")
        telescopio = Telescopio(**data)
        telescopio.save()
        return {"message": "Telescópio criado com sucesso", "data": convert_objectid(telescopio.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=dict)
async def get_all_telescopios(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Telescopio.objects.count()  # Contagem total de registros
    telescopios = Telescopio.objects.skip(skip).limit(limit)  # Paginação
    data = [convert_objectid(telescopio.to_mongo().to_dict()) for telescopio in telescopios]
    return {"total": total, "count": len(data), "telescopios": data}

@router.get("/{telescopio_id}", response_model=dict)
async def get_telescopio_by_id(telescopio_id: str):
    if not ObjectId.is_valid(telescopio_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    telescopio = Telescopio.objects(id=telescopio_id).first()
    if not telescopio:
        raise HTTPException(status_code=404, detail="Telescópio não encontrado")

    return {"data": convert_objectid(telescopio.to_mongo().to_dict())}

@router.get("/{telescopio_id}/filtrar", response_model=dict)
async def get_telescopios_by(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    nome: str = Query(None, description="Filtrar por nome"),
    tipo: str = Query(None, description="Filtrar por tipo"),
    localizacao: str = Query(None, description="Filtrar por localização"),
    diametro_min: float = Query(None, description="Filtrar por diâmetro mínimo"),
    diametro_max: float = Query(None, description="Filtrar por diâmetro máximo"),
    data_lancamento_inicio: str = Query(None, description="Filtrar por data de lançamento (início)"),
    data_lancamento_fim: str = Query(None, description="Filtrar por data de lançamento (fim)"),
    ordenacao: str = Query(None, description="Ordenar por campo (ex: nome, diametro)"),
    ordem_ascendente: bool = Query(True, description="Ordem ascendente (True) ou descendente (False)"),
):
    try:
        query = {}
        if nome:
            query["nome"] = {"$regex": nome, "$options": "i"}
        if tipo:
            query["tipo"] = {"$regex": tipo, "$options": "i"}
        if localizacao:
            query["localizacao"] = {"$regex": localizacao, "$options": "i"}
        if diametro_min is not None:
            query["diametro__gte"] = diametro_min
        if diametro_max is not None:
            query["diametro__lte"] = diametro_max
        if data_lancamento_inicio:
            try:
                data_lancamento_inicio = datetime.fromisoformat(data_lancamento_inicio)
                query["data_lancamento__gte"] = data_lancamento_inicio
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data de lançamento inicial inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")
        if data_lancamento_fim:
            try:
                data_lancamento_fim = datetime.fromisoformat(data_lancamento_fim)
                query["data_lancamento__lte"] = data_lancamento_fim
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data de lançamento final inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")

        total = Telescopio.objects(**query).count()

        if ordenacao:
            sinal = "" if ordem_ascendente else "-"
            telescopios = Telescopio.objects(**query).order_by(sinal + ordenacao).skip(skip).limit(limit)
        else:
            telescopios = Telescopio.objects(**query).skip(skip).limit(limit)

        data = [convert_objectid(telescopio.to_mongo().to_dict()) for telescopio in telescopios]
        return {"total": total, "count": len(data), "telescopios": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{telescopio_id}", response_model=dict)
async def get_telescopio_by_id(telescopio_id: str):
    try:
        if not ObjectId.is_valid(telescopio_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        telescopio = Telescopio.objects(id=telescopio_id).first()
        if not telescopio:
            raise HTTPException(status_code=404, detail="Telescópio não encontrado")

        return {"data": convert_objectid(telescopio.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{telescopio_id}", response_model=dict)
async def update_telescopio(telescopio_id: str, data: dict):
    if not ObjectId.is_valid(telescopio_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    telescopio = Telescopio.objects(id=telescopio_id).first()
    if not telescopio:
        raise HTTPException(status_code=404, detail="Telescópio não encontrado")

    telescopio.update(**data)
    telescopio.reload()
    return {"message": "Telescópio atualizado com sucesso", "data": convert_objectid(telescopio.to_mongo().to_dict())}

@router.delete("/{telescopio_id}", response_model=dict)
async def delete_telescopio(telescopio_id: str):
    if not ObjectId.is_valid(telescopio_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    telescopio = Telescopio.objects(id=telescopio_id).first()
    if not telescopio:
        raise HTTPException(status_code=404, detail="Telescópio não encontrado")

    telescopio.delete()
    return {"message": "Telescópio deletado com sucesso"}
