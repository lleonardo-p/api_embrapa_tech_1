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
data_type = "production"
query_opc = config['data_of_interest']['production']['opc']
query_sub_opc =""
mode = ""

crawler = EmbrapaCrawler(base_url, data_max, data_min, data_type, query_opc, query_sub_opc, mode)
crawler.crawler_seletetion("2022", "")
    

