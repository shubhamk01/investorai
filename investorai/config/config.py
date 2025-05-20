import yaml
import os

def load_config(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config
