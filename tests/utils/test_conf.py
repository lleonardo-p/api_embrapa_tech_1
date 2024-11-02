import pytest
import yaml
from unittest.mock import mock_open, patch
from utils.conf import Conf

@pytest.fixture
def mock_config():
    # Dados de configuração em formato YAML
    return """
    embrapa:
        url_base: "http://example.com/api"
    data_of_interest:
        processing:
            opc:
                - "processing"
                - "param"
            sub_options:
                option1: ["sub_param1", "desc1"]
        commercialization:
            opc:
                - "commercialization"
                - "param"
            sub_options:
                option2: ["sub_param2", "desc2"]
        importation:
            opc:
                - "importation"
                - "param"
            sub_options:
                option3: ["sub_param3", "desc3"]
        exportation:
            opc:
                - "exportation"
                - "param"
            sub_options:
                option4: ["sub_param4", "desc4"]
        production:
            opc:
                - "production"
                - "param"
            sub_options:
                option5: ["sub_param5", "desc5"]
    """

def test_load_config(mock_config):
    # Teste para verificar se a configuração é carregada corretamente
    with patch("builtins.open", mock_open(read_data=mock_config)):
        conf = Conf("fake_path.yaml")
        assert conf.config['embrapa']['url_base'] == "http://example.com/api"

def test_structing_data(mock_config):
    # Teste para verificar a estruturação dos dados
    with patch("builtins.open", mock_open(read_data=mock_config)):
        conf = Conf("fake_path.yaml")
        processed_data = conf.structing_data(conf.config['data_of_interest']['processing'])

        assert processed_data["processing"] == "param"
        assert "option1" in processed_data["sub_options"]
        assert processed_data["sub_options"]["option1"] == ("sub_param1", "desc1")

def test_get_properties(mock_config):
    # Teste para verificar se as propriedades estão sendo configuradas corretamente
    with patch("builtins.open", mock_open(read_data=mock_config)):
        conf = Conf("fake_path.yaml")
        conf.get_properties()

        assert conf.base_url == "http://example.com/api"
        assert conf.processing["processing"] == "param"
        assert "option1" in conf.processing["sub_options"]
        assert conf.commercialization["commercialization"] == "param"
        assert "option2" in conf.commercialization["sub_options"]

        assert conf.importation["importation"] == "param"
        assert conf.exportation["exportation"] == "param"
        assert conf.production["production"] == "param"
