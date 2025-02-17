from fastapi import APIRouter, HTTPException, Query
from models.observacao import Observacao

router = APIRouter()

@router.post("/", response_model=dict)
async def create_observacao(data: dict):
    observacao = Observacao(**data)
    observacao.save()
    return {"message": "Observação criada com sucesso", "data": observacao.to_mongo().to_dict()}

@router.get("/", response_model=dict)
async def get_all_observacoes(
    skip: int = Query(0, ge=0, description="Número de registros a ignorar"),
    limit: int = Query(10, gt=0, le=100, description="Número máximo de registros a retornar"),
):
    total = Observacao.objects.count()  # Contagem total de registros
    observacoes = Observacao.objects.skip(skip).limit(limit)  # Paginação
    data = [observacao.to_mongo().to_dict() for observacao in observacoes]
    return {"total": total, "count": len(data), "observacoes": data}

@router.get("/{observacao_id}", response_model=dict)
async def get_observacao_by_id(observacao_id: str):
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    return {"data": observacao.to_mongo().to_dict()}

@router.put("/{observacao_id}", response_model=dict)
async def update_observacao(observacao_id: str, data: dict):
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    observacao.update(**data)
    observacao.reload()
    return {"message": "Observação atualizada com sucesso", "data": observacao.to_mongo().to_dict()}

@router.delete("/{observacao_id}", response_model=dict)
async def delete_observacao(observacao_id: str):
    observacao = Observacao.objects(id=observacao_id).first()
    if not observacao:
        raise HTTPException(status_code=404, detail="Observação não encontrada")
    observacao.delete()
    return {"message": "Observação deletada com sucesso"}
