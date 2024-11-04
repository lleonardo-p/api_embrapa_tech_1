import yaml
from pathlib import Path

class Conf:
    def __init__(self, conf_path):
        self.base_url = ""
        self.processing = {}
        self.commercialization = {}
        self.importation = {}
        self.exportation = {}
        self.production = {}
        

        self.config_path = self._resolve_conf_path(conf_path)
        self.config = self._load_config(self.config_path)

    def _resolve_conf_path(self, conf_path):
        dir_path = Path(__file__).resolve().parent
        return dir_path.parent / conf_path  

    def _load_config(self, conf_path):
        with open(conf_path, 'r') as file:
            return yaml.safe_load(file)
        
    def structing_data(self, conf_dict):
        print(f"[structing_data] = {conf_dict}")
        route = conf_dict["opc"][0]
        param = conf_dict["opc"][1]
        sub_options = {}

        if "sub_options" in conf_dict:
            for opc in conf_dict["sub_options"]:
                sub_options[opc] = (conf_dict["sub_options"][opc][0], conf_dict["sub_options"][opc][1])

        return {
            route: param,
            "sub_options": sub_options
        }
        
    def get_properties(self):
        self.base_url = self.config['embrapa']['url_base']

        processing = self.config['data_of_interest']['processing']
        self.processing = self.structing_data(processing)

        commercialization = self.config['data_of_interest']['commercialization']
        self.commercialization = self.structing_data(commercialization)

        importation = self.config['data_of_interest']['importation']
        self.importation = self.structing_data(importation)

        exportation = self.config['data_of_interest']['exportation']
        self.exportation = self.structing_data(exportation)

        production = self.config['data_of_interest']['production']
        self.production = self.structing_data(production)
