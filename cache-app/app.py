from fastapi import FastAPI
from routes import main_router

app = FastAPI(
    title="cache-app",
    version="0.1.0",
    description="Cache app is an application to get data from any source and cache on redis", # noqaE501
)

app.include_router(main_router)


@app.get("/")
def HealthCheck():
    return {
        "message": "ok",
        "status": 200
    }
