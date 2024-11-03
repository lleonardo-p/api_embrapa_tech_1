import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.routes.routes import router


app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_get_production_data():
    response = client.get("/production/2024")
    assert response.status_code == 200

def test_get_processing_data():
    response = client.get("/processing/viniferas/2024")
    assert response.status_code == 200

def test_get_commercialization_data():
    response = client.get("/commercialization/2024")
    assert response.status_code == 200

def test_get_importation_data():
    response = client.get("/importation/vinho_mesa/2024")
    assert response.status_code == 200

def test_get_exportation_data():
    response = client.get("/exportation/vinho_mesa/2024")
    assert response.status_code == 200

def test_invalid_year_format():
    response = client.get("/production/20A4")
    assert response.status_code == 422  

def test_invalid_processing_option():
    response = client.get("/processing/invalid_option/2024")
    assert response.status_code == 422  

def test_invalid_importation_option():
    response = client.get("/importation/invalid_option/2024")
    assert response.status_code == 422  

def test_invalid_exportation_option():
    response = client.get("/exportation/invalid_option/2024")
    assert response.status_code == 422  
