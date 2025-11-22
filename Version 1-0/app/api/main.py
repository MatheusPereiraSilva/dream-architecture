from fastapi import FastAPI
from .routes_memory import router as memory_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="DREAM Memory Service",
        description="Serviço de memória episódica baseado no padrão DREAM.",
        version="0.1.0",
    )

    app.include_router(memory_router, prefix="/memory", tags=["memory"])
    return app


app = create_app()
