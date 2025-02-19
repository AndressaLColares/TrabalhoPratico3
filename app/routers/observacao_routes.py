from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from models.observacao import Observacao
from bson import ObjectId

router = APIRouter()

def convert_objectid(doc):
    if isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                doc[key] = str(value)
            elif isinstance(value, dict):
                convert_objectid(value)
            elif isinstance(value, list):
                doc[key] = [convert_objectid(item) if isinstance(item, (dict, list)) else str(item) if isinstance(item, ObjectId) else item for item in value]
    elif isinstance(doc, list):
        doc = [convert_objectid(item) if isinstance(item, (dict, list)) else str(item) if isinstance(item, ObjectId) else item for item in doc]
    return doc

@router.post("/", response_model=dict)
async def create_observacao(data: dict):
    try:
        if "datahora" in data and isinstance(data["datahora"], str):
            try:
                data["datahora"] = datetime.fromisoformat(data["datahora"])
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")

        for key in ["telescopio", "astronomo"]:
            if key in data and isinstance(data[key], str):
                if not ObjectId.is_valid(data[key]):
                    raise HTTPException(status_code=400, detail=f"ID inválido para {key}.")
                data[key] = ObjectId(data[key])

        if "fenomenos" in data and isinstance(data["fenomenos"], list):
            data["fenomenos"] = [ObjectId(f) if ObjectId.is_valid(f) else HTTPException(status_code=400, detail="ID de fenômeno inválido.") for f in data["fenomenos"]]
        
        observacao = Observacao(**data)
        observacao.save()
        return {"message": "Observação criada com sucesso", "data": convert_objectid(observacao.to_mongo().to_dict())}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=dict)
async def get_all_observacoes(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Observacao.objects.count()  
    observacoes = Observacao.objects.skip(skip).limit(limit)  
    data = [convert_objectid(obs.to_mongo().to_dict()) for obs in observacoes]
    return {"quantidade": total, "count": len(data), "observacoes": data}

@router.get("/{observacao_id}", response_model=dict)
async def get_observacao_by_id(observacao_id: str):
    if not ObjectId.is_valid(observacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    
    return convert_objectid(observacao.to_mongo().to_dict())

@router.get("/{observacao_id}/filtrar", response_model=dict)
async def get_observacoes_by(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),

    observador: str = Query(None, description="Filtrar por observador"),
    localizacao: str = Query(None, description="Filtrar por localização"),
    propriedades: str = Query(None, description="Filtrar por propriedades observadas"),
    datahora_inicio: str = Query(None, description="Filtrar por data e hora (início)"),
    datahora_fim: str = Query(None, description="Filtrar por data e hora (fim)"),

    ordenacao: str = Query(None, description="Ordenar por campo (ex: datahora, observador)"),
    ordem_ascendente: bool = Query(True, description="Ordem ascendente (True) ou descendente (False)"),
):
    try:
        query = {}
        if observador:
            query["observador"] = {"$regex": observador, "$options": "i"}
        if localizacao:
            query["localizacao"] = {"$regex": localizacao, "$options": "i"}
        if propriedades:
            query["propriedades_observadas"] = {"$regex": propriedades, "$options": "i"}
        if datahora_inicio:
            try:
                datahora_inicio = datetime.fromisoformat(datahora_inicio)
                query["datahora__gte"] = datahora_inicio
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data e hora inicial inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")
        if datahora_fim:
            try:
                datahora_fim = datetime.fromisoformat(datahora_fim)
                query["datahora__lte"] = datahora_fim
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de data e hora final inválido. Use 'YYYY-MM-DDTHH:MM:SS'.")

        total = Observacao.objects(**query).count()

        if ordenacao:
            sinal = "" if ordem_ascendente else "-"
            observacoes = Observacao.objects(**query).order_by(sinal + ordenacao).skip(skip).limit(limit)
        else:
            observacoes = Observacao.objects(**query).skip(skip).limit(limit)

        data = [convert_objectid(obs.to_mongo().to_dict()) for obs in observacoes]
        return {"quantidade": total, "count": len(data), "observacoes": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{observacao_id}/consulta_astronomo", response_model=dict)
async def get_in_astronomo(
    nome_astronomo: str = Query(None, description="Nome do astrônomo")
):
    try:
        observacoes = Observacao.objects(astronomo__nome__icontains=nome_astronomo)  # Case-insensitive
        resultados = []
        for observacao in observacoes:
            resultados.append({
                "datahora": observacao.datahora,
                "localizacao": observacao.localizacao,
                "astronomo": observacao.astronomo.nome if observacao.astronomo else None
            })

        return {"count": len(resultados), "observacoes": resultados}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{observacao_id}", response_model=dict)
async def update_observacao(observacao_id: str, data: dict):
    if not ObjectId.is_valid(observacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    
    for key in ["telescopio", "astronomo"]:
        if key in data and isinstance(data[key], str):
            if not ObjectId.is_valid(data[key]):
                raise HTTPException(status_code=400, detail=f"ID inválido para {key}.")
            data[key] = ObjectId(data[key])
    
    if "fenomenos" in data and isinstance(data["fenomenos"], list):
        data["fenomenos"] = [ObjectId(f) if ObjectId.is_valid(f) else HTTPException(status_code=400, detail="ID de fenômeno inválido.") for f in data["fenomenos"]]
    
    observacao.update(**data)
    observacao.reload()
    return {"message": "Observação atualizada com sucesso", "data": convert_objectid(observacao.to_mongo().to_dict())}

@router.delete("/{observacao_id}", response_model=dict)
async def delete_observacao(observacao_id: str):
    if not ObjectId.is_valid(observacao_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    
    observacao.delete()
    return {"message": "Observação excluída com sucesso"}