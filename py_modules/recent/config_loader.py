# config_loader.py
from dotenv import load_dotenv
import os

def load_config():
    load_dotenv('py_modules/recent/config.env')
    config = {
        'dict_id': os.environ['CLIENT_ID'],
        'symbol_id': os.environ['TENANT_ID'],
        'platform': os.environ['CLIENT_SECRET'],
        'url': os.environ["VAULT_URL"]
    }
    return config
