import requests
from bs4 import BeautifulSoup

class EmbrapaCrawler:
    def __init__(self, base_url, data_max, data_min, mode="inc"):
        self.base_url = base_url
        self.data_max = data_max
        self.data_min = data_min
        self.data_type = ""
        self.query_opc = ""
        self.query_sub_opc = ""
        self.mode = mode
        self.select_date = ""
        self.data_list = [] 
        self.processing = {    
                "viniferas": ("&subopcao=subopt_01","Viniferas"),
                "americana_hibri": ("&subopcao=subopt_02", "Americanas e hibridas"),
                "uva_mesa": ("&subopcao=subopt_03", "Uvas de mesa"),
                "sem_class": ("&subopcao=subopt_04", "Sem classificação")
            }
        self.importation = {
            "vinho_mesa": ("&subopcao=subopt_01", "Vinhos de mesa"),
            "espumante": ("&subopcao=subopt_02", "Espumantes"),
            "uvas_frescas": ("&subopcao=subopt_03", "Uvas frescas"),
            "uvas_passas": ("&subopcao=subopt_04", "Uvas passas"),
            "suco_uva": ("&subopcao=subopt_05", "Suco de uva")
        }

        self.exportation = {
            "vinho_mesa": ("&subopcao=subopt_01", "Vinhos de mesa"),
            "espumante": ("&subopcao=subopt_02", "Espumantes"),
            "uvas_frescas": ("&subopcao=subopt_03", "Uvas frescas"),
            "suco_uva": ("&subopcao=subopt_04", "Suco de uva")
        }

    def validate_date(self):
        pass

    def get_value_by_key(self, dict_crawler ,search_key):
        for key, (first, second) in dict_crawler.items():
            if first == search_key:
                return second
        return None  # Retorna None se não encontrar a chave

    def make_url(self, year_of_interest=""):
        target_url = f"{self.base_url}ano={year_of_interest}{self.query_opc}{self.query_sub_opc}"
        print(f"[make_url] {target_url}")
        return target_url

    def _production_and__commercialization(self, soup):
        produto_principal = None
        preco_produto = None

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
        
    def _processing(self, soup, classefication):
        produto_principal = None
        preco_produto = None

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
                    "Quantidade (kg)": preco_produto,
                    "Classeficacao": classefication
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
                    "Quantidade (kg)": quantidade_subproduto,
                    "Classeficacao": classefication
                })

        # retornar os dados ou salvar no db.
        n = 0
        for data in self.data_list:
            n += 1
            print(f"[{n}] - {data}]")
        #==============================================

    def _importation(self, soup, classefication):
        produto_principal = None
        preco_produto = None

        table = soup.find('table', class_='tb_base tb_dados')
        
        for linha in table.find_all("tr"):
            # Identifica os subprodutos
            subcelulas = linha.find_all("td")
            if subcelulas:
                pais = subcelulas[0].text.strip()
                quantidade_subproduto = subcelulas[1].text.strip()
                valor = subcelulas[2].text.strip()

                # Armazena cada produto e subproduto no formato desejado
                self.data_list.append({
                    "Pais": pais,
                    "Quantidade (kg)": quantidade_subproduto,
                    "valor": valor,
                    "Classeficacao": classefication
                })

        # retornar os dados ou salvar no db.
        n = 0
        for data in self.data_list:
            n += 1
            print(f"[{n}] - {data}]")
        #==============================================


    def crawler_seletetion(self, select_date):
        if self.data_type == "production":
            self._production_and__commercialization(select_date)

        if self.data_type == "commercialization":
            self._production_and__commercialization(select_date)

        if self.data_type == "processing":
            classefication = self.get_value_by_key(self.processing ,self.query_sub_opc)
            self._processing(select_date, classefication)

        if self.data_type == "importation":
            classefication = self.get_value_by_key(self.importation, self.query_sub_opc)
            self._importation(select_date, classefication)

        if self.data_type == "exportation":
            classefication = self.get_value_by_key(self.exportation, self.query_sub_opc)
            self._importation(select_date, classefication)



    def crawl(self, data_type="", query_opc="", query_sub_opc="", select_date=""):
        self.data_list = [] 
        self.data_type = data_type
        self.query_opc = query_opc
        self.query_sub_opc = query_sub_opc

        try:
            # Fazer a requisição
            url = self.make_url(select_date)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            self.crawler_seletetion(soup)


        except requests.RequestException as e:
            print(f"Error while accessing {url}: {e}")



