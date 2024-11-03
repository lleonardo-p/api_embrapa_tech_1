from fastapi import FastAPI
from api.routes import routes 
from fastapi.responses import JSONResponse

app = FastAPI()

# Inclua suas rotas
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Embrapa Crawler API!"}

@app.exception_handler(404)
async def custom_404_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Endpoint not found. Please check the URL."},
    )

from fastapi import FastAPI
from api.routes.routes import router as api_router

app = FastAPI()

# Inclui as rotas
app.include_router(api_router)

# Roda a aplicação
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

