# test_embrapa_crawler.py

import pytest
import requests_mock
from bs4 import BeautifulSoup
from datetime import datetime
from embrapa_crawler.crawler import EmbrapaCrawler

# A mock config object to provide configurations for the crawler
class MockConfig:
    base_url = "https://example.com/"
    production = {"production": "/production", "sub_options": {}}
    processing = {"processing": "/processing", "sub_options": {"01": ("&subopcao=subopt_01", "Viniferas")}}
    commercialization = {"commercialization": "/commercialization", "sub_options": {}}
    importation = {"importation": "/importation", "sub_options": {}}
    exportation = {"exportation": "/exportation", "sub_options": {}}

@pytest.fixture
def crawler():
    config = MockConfig()
    return EmbrapaCrawler(config=config)

def test_make_url(crawler):
    crawler.route = "processing"
    crawler.query_opc = "01"
    url = crawler.make_url("2023")
    assert url == "https://example.com/ano=2023/processing&subopcao=subopt_01"

def test_get_value_by_key(crawler):
    value = crawler._get_value_by_key(crawler.processing, "01")
    assert value == "Viniferas"

def test_parse_table_rows():
    html = '''
    <html>
    <body>
        <table class="tb_base tb_dados">
            <tr><td class="tb_item">Product A</td><td class="tb_item">100</td></tr>
            <tr><td class="tb_item">Product B</td><td class="tb_item">200</td></tr>
        </table>
    </body>
    </html>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    crawler = EmbrapaCrawler(MockConfig())
    rows = crawler._parse_table_rows(soup, "tb_base tb_dados")
    assert len(rows) == 2

def test_process_rows(crawler):
    html = '''
    <html>
    <body>
        <tr><td class="tb_item">Product A</td><td class="tb_item">100</td></tr>
    </body>
    </html>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all("tr")
    crawler._process_rows(rows, main_column="tb_item")
    assert len(crawler.data_list) == 1
    assert crawler.data_list[0]["Produto"] == "Product A"
    assert crawler.data_list[0]["Quantidade"] == "100"

@pytest.mark.parametrize("route, expected_output", [
    ("production", "Production called"),
    ("processing", "Processing called"),
    ("exportation", "Exportation called"),
])
def test_crawler_selection(mocker, crawler, route, expected_output):
    # Mock specific methods to test that they are called correctly based on the route
    mock_production = mocker.patch.object(crawler, '_production_and_commercialization')
    mock_processing = mocker.patch.object(crawler, '_processing')
    mock_importation = mocker.patch.object(crawler, '_importation_or_exportation')

    crawler.route = route
    crawler.query_opc = "01"
    crawler.crawler_selection(soup=None, year="2023")

    if route == "production":
        mock_production.assert_called_once()
    elif route == "processing":
        mock_processing.assert_called_once()
    else:
        mock_importation.assert_called_once()

