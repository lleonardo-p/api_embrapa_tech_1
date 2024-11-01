import requests
from bs4 import BeautifulSoup
from datetime import datetime

class EmbrapaCrawler:
    def __init__(self, base_url, mode="inc"):
        self.base_url = base_url
        self.data_type = ""
        self.query_opc = ""
        self.query_sub_opc = ""
        self.mode = mode
        self.select_date = ""
        self.data_list = []
        self.processing = {
            "viniferas": ("&subopcao=subopt_01", "Viniferas"),
            "americana_hibri": ("&subopcao=subopt_02", "Americanas e híbridas"),
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
   
    def _get_value_by_key(self, dict_crawler ,search_key):
        for _, (first, second) in dict_crawler.items():
            if first == search_key:
                return second
        return None  

    def make_url(self, year_of_interest=""):
        url = f"{self.base_url}ano={year_of_interest}{self.query_opc}{self.query_sub_opc}"
        print(f"[make_url] {url}")
        return url

    def _parse_table_rows(self, soup, table_class):
        table = soup.find('table', class_=table_class)
        if not table:
            print(f"Table with class '{table_class}' not found.")
            return []
        rows = table.find_all("tr")
        if not rows:
            print("No rows found in the table.")
        return rows

    def _process_rows(self, rows, main_column, sub_column=None, extra_info=None):
        for row in rows:
            cells = row.find_all("td", class_=main_column)
            if cells:
                main_product = cells[0].text.strip()
                main_value = cells[1].text.strip() if len(cells) > 1 else "N/A"
                self.data_list.append({
                    "Produto": main_product,
                    "Subproduto": "---",
                    "Quantidade": main_value,
                    **(extra_info or {})
                })

            if sub_column:
                sub_cells = row.find_all("td", class_=sub_column)
                if sub_cells:
                    sub_product = sub_cells[0].text.strip()
                    sub_quantity = sub_cells[1].text.strip() if len(sub_cells) > 1 else "N/A"
                    self.data_list.append({
                        "Produto": main_product,
                        "Subproduto": sub_product,
                        "Quantidade": sub_quantity,
                        **(extra_info or {})
                    })

    def _production_and_commercialization(self, soup, year):
        rows = self._parse_table_rows(soup, "tb_base tb_dados")
        extra_info = {"Ano": year}
        self._process_rows(rows, "tb_item", "tb_subitem", extra_info)

    def _processing(self, soup, classification, year):
        rows = self._parse_table_rows(soup, "tb_base tb_dados")
        extra_info = {"Classificação": classification, "Ano": year}
        self._process_rows(rows, "tb_item", "tb_subitem", extra_info)

    def _importation_or_exportation(self, soup, classification, year):
        rows = self._parse_table_rows(soup, "tb_base tb_dados")
        for row in rows:
            cells = row.find_all("td")
            if cells and len(cells) >= 3:
                country = cells[0].text.strip()
                quantity = cells[1].text.strip()
                value = cells[2].text.strip()
                self.data_list.append({
                    "País": country,
                    "Quantidade (kg)": quantity,
                    "Valor": value,
                    "Classificação": classification,
                    "Ano": year
                })

    def crawler_selection(self, soup, year):
        classification = None
        if self.data_type in ["processing", "importation", "exportation"]:
            data_map = getattr(self, self.data_type, {})
            classification = self._get_value_by_key(data_map, self.query_sub_opc)

        if self.data_type in ["production", "commercialization"]:
            self._production_and_commercialization(soup, year)
        elif self.data_type == "processing":
            self._processing(soup, classification, year)
        elif self.data_type in ["importation", "exportation"]:
            self._importation_or_exportation(soup, classification, year)

    def crawl(self, data_type="", query_opc="", query_sub_opc="", select_date=""):
        self.data_list = []
        self.data_type = data_type
        self.query_opc = query_opc
        self.query_sub_opc = query_sub_opc
        url = self.make_url(select_date)

        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            soup = BeautifulSoup(response.content, 'html.parser')
            self.crawler_selection(soup, select_date)
        except requests.RequestException as e:
            print(f"Error while accessing {url}: {e}")
        except Exception as e:
            print(f"An error occurred during crawling: {e}")
        else:
            print(f"Crawling completed successfully for URL: {url}")

        # Display gathered data
        return self.data_list 