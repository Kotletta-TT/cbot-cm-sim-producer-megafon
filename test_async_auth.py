import asyncio
from asyncio import tasks
import aiohttp
from aiohttp import cookiejar
from config import config_parser
from models import Contract
from generators import get_urls_simList

CONTRACTS = config_parser('contracts.yaml')


async def login(contract: Contract):
    method = 'POST'
    # contentType = "application/x-www-form-urlencoded;charset=UTF-8" - вроде как не нужны, aiohttp сам их генерирует
    # headers = {'Content-Type': contentType}
    response = await contract.session.request(method=method, url=contract.login_url, data=contract.form_data) # , headers=headers)
    # test = await response.json()
    # print(test)
    # return contract
    simcards = await contract.session.get('https://b2blk.megafon.ru/ws/v1.0/subscriber/mobile/list?from=0&size=1')
    simcards_json = await simcards.json()
    contract_sim_count = int(simcards_json['data']['count'])
    

async def all_login():
    tasks = []
    #contracts_obj = []
    for contract in CONTRACTS:
        contract_obj = Contract(**contract, session=aiohttp.ClientSession(), form_data=aiohttp.FormData())
        tasks.append(login(contract_obj))
    #   contracts_obj.append(contract_obj)
    await asyncio.gather(*tasks)
    

    # return contracts_obj

async def get_list_sim(contract: Contract):
        response = await contract.session.get('https://b2blk.megafon.ru/ws/v1.0/subscriber/mobile/list?from=0&size=1')
        test = await response.json()
        print(test)       

async def get_all_simcards(contracts):
    tasks = []
    for contract in contracts:
        tasks.append(contract.get_list_sim())
    await asyncio.gather(*tasks)


asyncio.run(all_login())

