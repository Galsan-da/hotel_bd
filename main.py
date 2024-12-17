import uvicorn
from fastapi import FastAPI
#from fastapi.openapi.docs import get_swagger_ui_html

from hotels import router as router_hotels

# Создаем экземпляр FastAPI приложения
app = FastAPI()

app.include_router(router_hotels)

#@app.get("/docs", include_in_schema=False)
#async def custom_swagger_ui_html(): ...

# Точка входа для запуска приложения
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
