import yaml

def read_config() -> dict:
    with open("config.yaml", "r", encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

# Load the configuration file
GLOBAL_CONFIG = read_config()