from fastapi import FastAPI
from api_embrapa_tech_1.api.routes import routes 
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

