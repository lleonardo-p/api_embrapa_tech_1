import requests
from bs4 import BeautifulSoup

class EmbrapaCrawler:
    def __init__(self, config=""):
        self.base_url = config.base_url
        self.route = ""
        self.query_opc = ""
        self.select_date = ""
        self.data_list = []
        self.production = config.production
        self.processing = config.processing
        self.commercialization = config.commercialization
        self.importation = config.importation
        self.exportation = config.exportation
   
    
    def validate_route(self):
        data_map = getattr(self, self.route, {})

        if not data_map:
            return False

        has_sub_options = data_map.get("sub_options")
        if has_sub_options and self.query_opc not in has_sub_options:
            return False

        return True


    
    def _get_value_by_key(self, dict_crawler ,search_key):
        sub_opc = dict_crawler["sub_options"]
        if len(sub_opc) > 0:
            if search_key in sub_opc:
                return sub_opc[search_key][1]

        return None  

    def make_url(self, year_of_interest=""):
        data_map = getattr(self, self.route, {})
        route = data_map[self.route]

        if len(data_map["sub_options"]) > 0:
            if self.query_opc in data_map['sub_options']:
                opc = data_map['sub_options'][self.query_opc][0]
        else:
            opc=""
        
        url = f"{self.base_url}ano={year_of_interest}{route}{opc}"
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
        if self.route in ["processing", "importation", "exportation"]:
            data_map = getattr(self, self.route, {})
            classification = self._get_value_by_key(data_map, self.query_opc)

        if self.route in ["production", "commercialization"]:
            self._production_and_commercialization(soup, year)
        elif self.route == "processing":
            self._processing(soup, classification, year)
        elif self.route in ["importation", "exportation"]:
            self._importation_or_exportation(soup, classification, year)

    def crawl(self, route="", opc="", select_date=""):
        self.data_list = []
        self.route = route
        self.query_opc = opc
        if not self.validate_route():
            return "URL não é valida"

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

        return self.data_list 