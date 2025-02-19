from fastapi import APIRouter
from routers import (
    astronomo_routes,
    estrela_routes,
    exoplaneta_routes,
    fenomeno_celestial_routes,
    observacao_routes,
    planeta_routes,
    telescopio_routes,
)

app = APIRouter()

app.include_router(astronomo_routes.router, prefix="/astronomos", tags=["Astronomos"])
app.include_router(estrela_routes.router, prefix="/estrelas", tags=["Estrelas"])
app.include_router(exoplaneta_routes.router, prefix="/exoplanetas", tags=["Exoplanetas"])
app.include_router(fenomeno_celestial_routes.router, prefix="/fenomenos", tags=["Fenômenos Celestiais"])
app.include_router(observacao_routes.router, prefix="/observacoes", tags=["Observações"])
app.include_router(planeta_routes.router, prefix="/planetas", tags=["Planetas"])
app.include_router(telescopio_routes.router, prefix="/telescopios", tags=["Telescópios"])
