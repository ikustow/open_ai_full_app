"""
FastAPI приложение для работы с AI агентами
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import api_router

app = FastAPI(
    title="AI Agents API",
    version="1.0.0",
    description="API для работы с AI агентами",
    openapi_url="/api/v1/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение API роутов
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "AI Agents API", "status": "running"}

@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
