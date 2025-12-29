import uvicorn 
from fastapi import FastAPI 
from app.api.v1.router import router as v1_router

app = FastAPI(title="FinGuard API")

@app.get("/health")
def health_check():
    return {"status":"ok"}

app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)