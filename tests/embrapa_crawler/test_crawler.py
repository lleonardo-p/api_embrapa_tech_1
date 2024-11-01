import pytest
from bs4 import BeautifulSoup
from embrapa_crawler.crawler import EmbrapaCrawler

@pytest.fixture
def crawler():
    return EmbrapaCrawler(base_url="http://example.com/")


def mock_html_page():
    return '''
        <html>
            <body>
                <table class="tb_base tb_dados">
                    <tr><td class="tb_item">Produto Principal</td><td class="tb_item">1000</td></tr>
                    <tr><td class="tb_subitem">Subproduto</td><td class="tb_subitem">500</td></tr>
                </table>
            </body>
        </html>
    '''


def test_make_url(crawler):
    url = crawler.make_url("2024")
    assert url == "http://example.com/ano=2024"


def test_get_value_by_key(crawler):
    value = crawler._get_value_by_key(crawler.processing, "&subopcao=subopt_01")
    assert value == "Viniferas"
    
    value_none = crawler._get_value_by_key(crawler.processing, "&subopcao=invalid")
    assert value_none is None


def test_parse_table_rows(crawler):
    soup = BeautifulSoup(mock_html_page(), "html.parser")
    rows = crawler._parse_table_rows(soup, "tb_base tb_dados")
    assert len(rows) == 2  # Deve encontrar 2 linhas na tabela


def test_process_rows(crawler):
    soup = BeautifulSoup(mock_html_page(), "html.parser")
    rows = crawler._parse_table_rows(soup, "tb_base tb_dados")
    crawler._process_rows(rows, "tb_item", "tb_subitem")
    assert len(crawler.data_list) == 2  # Deve ter 2 produtos/subprodutos

def test_crawl(requests_mock, crawler):
    url = "http://example.com/ano=2024"
    requests_mock.get(url, text=mock_html_page())
    result = crawler.crawl(data_type="production", select_date="2024")
    assert len(result) == 2  # Deve conter os dados extraídos da página
    assert result[0]["Produto"] == "Produto Principal"
    assert result[1]["Subproduto"] == "Subproduto"
