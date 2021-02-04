import pika
import json
import time
from models import Contract, Sim
from MegafonAPI import LK
from config import RABBIT_HOST, RABBIT_PORT, RABBIT_QUEUE, LOG_NAME, TIMEOUT_REQUEST, conf_parser
from pprint import pprint
from log_init import log_on

import traceback

logger = log_on(LOG_NAME)
DATA_ACCESS = conf_parser('contracts.yaml')



def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except (KeyError, IndexError):
            return False
    return True


def smart_timeout(attempts):
    if attempts <= 10:
        return time.sleep(10)
    else:
        return time.sleep(60)


def connect_rabbit_queue(fn):
    def wrapped():
        attempts = 0
        while True:
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT))
                channel = connection.channel()
                logger.debug(f'Connect to RabbitMQ address: {RABBIT_HOST}')
                attempts = 0
                break
            except:
                logger.error(f'RabbitMQ CONNECTION ERROR: {RABBIT_HOST}')
                smart_timeout(attempts)
                attempts += 1

        channel.queue_declare(queue=RABBIT_QUEUE)
        logger.debug(f'Queue select: {RABBIT_QUEUE}')
        fn(channel)
        connection.close()

    return wrapped


@connect_rabbit_queue
def request_api(channel):
    for obj in DATA_ACCESS:
        logger.info(f" Request to account: {obj['login']}")
        lk = LK(**obj)

        if lk.getSimCards():
            lk.getSimServicesInfo(lk.simcards)
            lk.getSimBalanceInfo(lk.simcards)
            lk.getSimRemainsInfo(lk.simcards)
            lk.getSimDCRulesInfo(lk.simcards)
            for sim in lk.simcards:
                try:
                    active = True if sim['raw']['status'] == "Активный (Действующий)" else False
                    balance = sim['raw']['balance']['value'] if keys_exists(sim, 'raw', 'balance','value') else None
                    services = sim['services'] if 'services' in sim else None
                    minute_remain = sim['finance']['discounts']['data'][0]['spend'] if keys_exists(sim, 'finance', 'discounts', 'data', 0, 'spend') else None
                    minute_total = sim['finance']['discounts']['data'][0]['total'] if keys_exists(sim, 'finance', 'discounts', 'data', 0, 'total') else None
                    accured = sim['finance']['balance']['data']['amountTotal'] if keys_exists(sim, 'finance','balance','data','amountTotal') else None
                    subscr_fee = sim['finance']['balance']['data']['monthChargeRTPL'] if keys_exists(sim, 'finance', 'balance', 'data', 'monthChargeRTPL') else None
                    send_sim = Sim(
                        id=sim['id'],
                        phone=sim['msisdn'],
                        active=active,
                        balance=balance,
                        services=services,
                        rate=sim['raw']['ratePlan'],
                        minute_remain=minute_remain,
                        minute_total=minute_total,
                        accured=accured,
                        subscr_fee=subscr_fee
                    )
                    message = json.dumps(send_sim.__dict__)
                    channel.basic_publish(exchange='', routing_key=RABBIT_QUEUE, body=message)
                    logger.info(f'Send sim: {send_sim.id} - {send_sim.phone} queue: {RABBIT_QUEUE}')
                except Exception:
                    
                    logger.error(f"Don`t send data to queue sim : {sim['msisdn']}, contract: {obj['login']}")
        else:
            logger.warning(f'NO CONNECTION to {obj["provider"]} OR no TRUNKS to {obj["obj"]}')


def main_loop():
    while True:
        request_api()
        time.sleep(TIMEOUT_REQUEST)


if __name__ == '__main__':
    main_loop()