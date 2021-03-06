import yaml


def conf_parser(file):
    with open(file, 'r') as f:
        return yaml.safe_load(f)

conf = conf_parser('config/config.yaml')

RABBIT_HOST = conf['rabbitmq']['host']
RABBIT_PORT = conf['rabbitmq']['port']
RABBIT_QUEUE = conf['rabbitmq']['queue']
LOG_LEVEL = conf['log-level']
LOG_NAME = conf['log-name']
TIMEOUT_REQUEST = conf['timeout-request']