# import yaml
# from MegafonAPI import LK
# from time import time

# startTime = time()
# lk = LK("b2blk.megafon.ru", "9257278007", "u4828m")
# if lk.getSimCards():
#     lk.getSimServicesInfo(lk.simcards)
#     for i in lk.simcards:
#         print(i)
# endTime = time()
# print(str(endTime - startTime))

# import asyncio
# import aiohttp
import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=10, maxsize=200, block=block)

method = "POST"
contentType = "application/x-www-form-urlencoded;charset=UTF-8"
address = "b2blk.megafon.ru"
session = requests.Session()
adapter = HttpAdapter()
session.mount(f"https://{address}", adapter=adapter)
login_address = f"https://{address}/ws/v1.0/auth/process" 
payload = "captchaTime=undefined&password=u4828m&username=9257278007"
headers = {'Content-Type': contentType}


a =session.request(method=method, url=login_address, data=payload.encode('utf-8'), headers=headers)
print(a.text)
if "XSRF_TOKEN" in session.cookies:
    session.headers["x-csrf-token"] = session.cookies["XSRF_TOKEN"]
b = session.request(method='GET', url='https://b2blk.megafon.ru/ws/v1.0/subscriber/mobile/list?from=0&size=1')
print(b.text)


# async def fetch(url, session):
#     response = await session.get(url)
#     html = await response.text()
#     return html


# async def main(urls):
#     session = aiohttp.ClientSession()
#     tasks = []
#     for url in urls:
#         tasks.append(fetch(url, session))
#     # await session.close()
    
#     await asyncio.gather(*tasks)


# URLS = ['https://google.ru/', 'https://yandex.ru/', 'https://github.com/']

# asyncio.run(main(URLS))




