import uvicorn 
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.router import router as v1_router
from app.core.Utils.phone import InvalidPhoneNumber

app = FastAPI(title="FinGuard API")

@app.exception_handler(InvalidPhoneNumber)
async def invalid_phone_handler(request: Request, exc: InvalidPhoneNumber):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )

@app.get("/health")
def health_check():
    return {"status":"ok"}

app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)