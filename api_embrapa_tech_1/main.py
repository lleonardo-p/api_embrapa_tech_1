import yaml
from embrapa_crawler.crawler import EmbrapaCrawler

# Função para carregar as configurações do arquivo YAML
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Carregar as configurações do prod.yml
config = load_config("config/prod.yml")

# Acessar uma configuração
base_url = config['embrapa']['url_base']
print(base_url)


base_url="http://vitibrasil.cnpuv.embrapa.br/index.php?"

base_url  = config['embrapa']['url_base']
data_max = config['embrapa']['data_max']
data_min = config['embrapa']['data_min']
mode = ""

crawler = EmbrapaCrawler(base_url)

print(f"[*] Production::::::")
data_type = "production"
query_opc = config['data_of_interest']['production']['opc']
query_sub_opc =""
result = crawler.crawl(data_type , query_opc, query_sub_opc, "2022")
print(result[2])


print(f"[*] Commercialization::::::")
data_type = "commercialization"
query_opc = config['data_of_interest']['commercialization']['opc']
query_sub_opc =""
result = crawler.crawl(data_type , query_opc, query_sub_opc, "2022")
print(result[2])

print(f"[*] Processing::::::")
data_type = "processing"
query_opc = config['data_of_interest']['processing']['opc']
query_sub_opc = config['data_of_interest']['processing']['viniferas']
result = crawler.crawl(data_type , query_opc, query_sub_opc, "2023")
print(result[2])


print(f"[*] Importation::::::")
data_type = "importation"
query_opc = config['data_of_interest']['importation']['opc']
query_sub_opc = config['data_of_interest']['importation']['vinho_mesa']
result = crawler.crawl(data_type , query_opc, query_sub_opc, "2023")
print(result[2])


print(f"[*] Exportation::::::")
data_type = "exportation"
query_opc = config['data_of_interest']['exportation']['opc']
query_sub_opc = config['data_of_interest']['exportation']['vinho_mesa']
result = crawler.crawl(data_type , query_opc, query_sub_opc, "2023")
print(result[2])

    

