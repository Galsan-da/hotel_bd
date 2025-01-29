import uvicorn
import sys

from pathlib import Path
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth

# Создаем экземпляр FastAPI приложения
app = FastAPI(docs_url=None)

app.include_router(router_auth)
app.include_router(router_hotels)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():...

# Точка входа для запуска приложения
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
