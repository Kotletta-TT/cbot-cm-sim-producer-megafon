import yaml


def config_parser(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)