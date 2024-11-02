from fastapi import APIRouter
from embrapa_crawler.crawler import EmbrapaCrawler
from utils.conf import Conf

# Carregar as configurações do prod.yml
config = Conf("config/prod.yml")
config.get_properties()
crawler = EmbrapaCrawler(config)

router = APIRouter()

@router.get("/production/{year}")
def get_data(year: str):
    value = "production"
    result = crawler.crawl(value, "", year)
    return result


@router.get("/processing/{opc}/{year}")
def get_data(opc: str, year: str):
    value = "processing"
    result = crawler.crawl(value, opc, year)
    return result


@router.get("/commercialization/{year}")
def get_data(year: str):
    value = "commercialization"
    result = crawler.crawl(value, "", year)
    return result


@router.get("/importation/{opc}/{year}")
def get_data(opc: str, year: str):
    value = "importation"
    result = crawler.crawl(value, opc, year)
    return result

@router.get("/exportation/{opc}/{year}")
def get_data(opc: str, year: str):
    value = "exportation"
    result = crawler.crawl(value, opc, year)
    return result