from fastapi import APIRouter, Path
from enum import Enum
from api_embrapa_tech_1.embrapa_crawler.crawler import EmbrapaCrawler
from api_embrapa_tech_1.utils.conf import Conf

config = Conf("utils/config/prod.yml")
config.get_properties()
crawler = EmbrapaCrawler(config)

router = APIRouter()

class ProcessingOptions(str, Enum):
    viniferas = "viniferas"
    americana_hibri = "americana_hibri"
    uva_mesa = "uva_mesa"
    sem_class = "sem_class"

class ImportationOptions(str, Enum):
    vinho_mesa = "vinho_mesa"
    espumante = "espumante"
    uvas_frescas = "uvas_frescas"
    uvas_passas = "uvas_passas"
    suco_uva = "suco_uva"

class ExportationOptions(str, Enum):
    vinho_mesa = "vinho_mesa"
    espumante = "espumante"
    uvas_frescas = "uvas_frescas"
    suco_uva = "suco_uva"

@router.get("/production/{year}",
            summary="Get production data",
            description="Fetch production data for a specified year in the format YYYY.")
def get_data(year: str = Path(..., pattern=r"^\d{4}$", description="Year in format YYYY, e.g., 2024")):
    value = "production"
    result = crawler.crawl(value, "", year)
    return result


@router.get("/processing/{opc}/{year}",
            summary="Get processing data",
            description="Fetch processing data for a specified year and operation type (opc). Available options: viniferas, americana_hibri, uva_mesa, sem_class.")
def get_data(opc: ProcessingOptions, year: str = Path(..., pattern=r"^\d{4}$", description="Year in format YYYY, e.g., 2024")):
    value = "processing"
    result = crawler.crawl(value, opc, year)
    return result


@router.get("/commercialization/{year}",
            summary="Get commercialization data",
            description="Fetch commercialization data for a specified year in the format YYYY.")
def get_data(year: str = Path(..., pattern=r"^\d{4}$", description="Year in format YYYY, e.g., 2024")):
    value = "commercialization"
    result = crawler.crawl(value, "", year)
    return result


@router.get("/importation/{opc}/{year}",
            summary="Get importation data",
            description="Fetch importation data for a specified year and operation type (opc). Available options: vinho_mesa, espumante, uvas_frescas, uvas_passas, suco_uva.")
def get_data(opc: ImportationOptions, year: str = Path(..., pattern=r"^\d{4}$", description="Year in format YYYY, e.g., 2024")):
    value = "importation"
    result = crawler.crawl(value, opc, year)
    return result

@router.get("/exportation/{opc}/{year}",
            summary="Get exportation data",
            description="Fetch exportation data for a specified year and operation type (opc). Available options: vinho_mesa, espumante, uvas_frescas, suco_uva.")
def get_data(opc: ExportationOptions, year: str = Path(..., pattern=r"^\d{4}$", description="Year in format YYYY, e.g., 2024")):
    value = "exportation"
    result = crawler.crawl(value, opc, year)
    return result
