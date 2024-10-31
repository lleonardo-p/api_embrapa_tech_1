import requests
from bs4 import BeautifulSoup

class EmbrapaCrawler:
    def __init__(self, base_url, data_max, data_min, data_type, query_opc, query_sub_opc="", mode="inc"):
        self.base_url = base_url
        self.data_max = data_max
        self.data_min = data_min
        self.data_type = data_type
        self.query_opc = query_opc
        self.query_sub_opc = query_sub_opc
        self.mode = mode
        self.select_date = ""
        self.data_list = [] 

    def validate_date(self):
        pass

    def test_url():
        pass

    def _production(self, select_date):
        url = self.make_url(select_date)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        produto_principal = None

        table = soup.find('table', class_='tb_base tb_dados')
        
        for linha in table.find_all("tr"):
            celulas = linha.find_all("td", class_="tb_item")
        
            # Identifica o produto principal
            if celulas:
                produto_principal = celulas[0].text.strip()
                preco_produto = celulas[1].text.strip()
                self.data_list.append({
                    "Produto": produto_principal,
                    "Subproduto": "---",
                    "Quantidade": preco_produto
                })

            # Identifica os subprodutos
            subcelulas = linha.find_all("td", class_="tb_subitem")
            if subcelulas:
                subproduto = subcelulas[0].text.strip()
                quantidade_subproduto = subcelulas[1].text.strip()

                # Armazena cada produto e subproduto no formato desejado
                self.data_list.append({
                    "Produto": produto_principal,
                    "Subproduto": subproduto,
                    "Quantidade": quantidade_subproduto
                })

        # retornar os dados ou salvar no db.
        n = 0
        for data in self.data_list:
            n += 1
            print(f"[{n}] - {data}]")
        #==============================================
        
    def _commercialization(self):
        pass


    def crawler_seletetion(self, select_date, select_sub_opc=""):
        if self.data_type == "production":
            self._production(select_date)

        if self.data_type == "commercialization":
            self._commercialization(select_date, select_sub_opc)

    def make_url(self, year_of_interest=""):
        target_url = f"{self.base_url}ano={year_of_interest}{self.query_opc}{self.query_sub_opc}"
        print(f"[make_url] {target_url}")
        return target_url #= f"{self.base_url}{self.query_opc}&ano={year_of_interest}"

    def crawl(self, data_of_interest="", year_of_interest=""):
        url = self.make_url(data_of_interest, year_of_interest)

        print(f"Crawling: {url}")
        try:
            # Fazer a requisição
            response = requests.get(url)
            response.raise_for_status()  # Levanta um erro para respostas de erro

            # Analisar o conteúdo HTML
            soup = BeautifulSoup(response.content, 'html.parser')


        except requests.RequestException as e:
            print(f"Error while accessing {url}: {e}")



