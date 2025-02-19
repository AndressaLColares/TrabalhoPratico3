from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models.planeta import Planeta
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    """Converte ObjectId para string em um dicionário do MongoDB."""
    if doc and "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.post("/", response_model=dict)
async def create_planeta(data: dict):
    try:
        if "data_descoberta" in data and isinstance(data["data_descoberta"], str):
            try:
                data["data_descoberta"] = datetime.fromisoformat(data["data_descoberta"])
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")
    
        planeta = Planeta(**data)
        planeta.save()
        return {"message": "Planeta criado com sucesso", "data": convert_objectid(planeta.to_mongo().to_dict())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=dict)
async def get_all_planetas(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Planeta.objects.count()  # Contagem total de registros
    planetas = Planeta.objects.skip(skip).limit(limit)  # Paginação
    data = [convert_objectid(planeta.to_mongo().to_dict()) for planeta in planetas]
    return {"total": total, "count": len(data), "planetas": data}

@router.get("/{planeta_id}", response_model=dict)
async def get_planeta_by_id(planeta_id: str):
    if not ObjectId.is_valid(planeta_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")

    return {"data": convert_objectid(planeta.to_mongo().to_dict())}

@router.get("/{planeta_id}/filtrar", response_model=dict)
async def get_planetas_by(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
    nome: str = Query(None, description="Filtrar por nome"),
    tipo: str = Query(None, description="Filtrar por tipo"),
    periodo_orbital_min: float = Query(None, description="Filtrar por período orbital (mínimo)"),
    periodo_orbital_max: float = Query(None, description="Filtrar por período orbital (máximo)"),
    raio_min: float = Query(None, description="Filtrar por raio (mínimo)"),
    raio_max: float = Query(None, description="Filtrar por raio (máximo)"),
    massa_min: float = Query(None, description="Filtrar por massa (mínimo)"),
    massa_max: float = Query(None, description="Filtrar por massa (máximo)"),
    data_descoberta_inicio: str = Query(None, description="Filtrar por data de descoberta (início)"),
    data_descoberta_fim: str = Query(None, description="Filtrar por data de descoberta (fim)"),
    ordenacao: str = Query(None, description="Ordenar por campo (ex: nome, periodo_orbital)"),
    ordem_ascendente: bool = Query(True, description="Ordem ascendente (True) ou descendente (False)"),
):
    try:
        query = {}
        if nome:
            query["nome"] = {"$regex": nome, "$options": "i"}
        if tipo:
            query["tipo"] = {"$regex": tipo, "$options": "i"}
        if periodo_orbital_min is not None:
            query["periodo_orbital__gte"] = periodo_orbital_min
        if periodo_orbital_max is not None:
            query["periodo_orbital__lte"] = periodo_orbital_max
        if raio_min is not None:
            query["raio__gte"] = raio_min
        if raio_max is not None:
            query["raio__lte"] = raio_max
        if massa_min is not None:
            query["massa__gte"] = massa_min
        if massa_max is not None:
            query["massa__lte"] = massa_max
        if data_descoberta_inicio:
            try:
                data_descoberta_inicio = datetime.fromisoformat(data_descoberta_inicio)
                query["data_descoberta__gte"] = data_descoberta_inicio
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data de descoberta inicial inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")
        if data_descoberta_fim:
            try:
                data_descoberta_fim = datetime.fromisoformat(data_descoberta_fim)
                query["data_descoberta__lte"] = data_descoberta_fim
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data de descoberta final inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")

        total = Planeta.objects(**query).count()

        if ordenacao:
            sinal = "" if ordem_ascendente else "-"
            planetas = Planeta.objects(**query).order_by(sinal + ordenacao).skip(skip).limit(limit)
        else:
            planetas = Planeta.objects(**query).skip(skip).limit(limit)

        data = [convert_objectid(planeta.to_mongo().to_dict()) for planeta in planetas]
        return {"total": total, "count": len(data), "planetas": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{planeta_id}", response_model=dict)
async def update_planeta(planeta_id: str, data: dict):
    if not ObjectId.is_valid(planeta_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")

    planeta.update(**data)
    planeta.reload()
    return {"message": "Planeta atualizado com sucesso", "data": convert_objectid(planeta.to_mongo().to_dict())}

@router.delete("/{planeta_id}", response_model=dict)
async def delete_planeta(planeta_id: str):
    if not ObjectId.is_valid(planeta_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    planeta = Planeta.objects(id=planeta_id).first()
    if not planeta:
        raise HTTPException(status_code=404, detail="Planeta não encontrado")

    planeta.delete()
    return {"message": "Planeta deletado com sucesso"}
