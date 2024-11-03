from embrapa_crawler.crawler import EmbrapaCrawler
from utils.conf import Conf


# Carregar as configurações do prod.yml
config = Conf("config/prod.yml")
config.get_properties()
crawler = EmbrapaCrawler(config)

# result = crawler.crawl("processing" , "viniferas", "2023")
# print(result)
# print(len(result))

result = crawler.crawl("production" , "", "2023")
print(result)
print(len(result))


