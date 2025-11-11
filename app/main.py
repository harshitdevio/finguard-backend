from fastapi import FastAPI 
from app.api.v1 import routes_test

app = FastAPI(title="FinGuard API")

@app.get("/health")
def health_check():
    return {"status":"ok"}

app.include_router(routes_test.router, prefix="/v1")