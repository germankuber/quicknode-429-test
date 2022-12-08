import asyncio
import json
import threading

import aiohttp
import requests

response_200 = 0
response_429 = 0
json_object = json.loads("""
                       {
    "id": 1,
    "method": "eth_getTransactionByHash",
    "jsonrpc": "2.0",
    "params": ["0x1526b9542cc3eb1fcbbe091f299fd179f8f9eda9d24eed5a52500916f7b88734"
    ]
}""")
def send_request_raw():
    try:
        global json_object
        
        x = requests.post('https://prettiest-polished-wind.quiknode.pro/<id>/',
                        headers={
                            'Content-Type': 'application/json'
                        },
                        json =json_object)
        check_status(x.status_code)

    except Exception as inst :
        print(x.text)

def check_status(status_code:int):
    if status_code == 200:
        global response_200
        response_200 +=1
    elif status_code == 429:
        global response_429
        response_429 +=1
    print_result()
    
def print_result():
    global response_200
    global response_429
    print(f"200 : {response_200} - 429 : {response_429} - ")
async def request_aio():
    global json_object
    async with aiohttp.ClientSession() as session:
        async with session.post('https://prettiest-polished-wind.quiknode.pro/<id>/', 
                                 headers={
                            'Content-Type': 'application/json'
                        },
                                 json = json_object) as response:
            check_status(response.status)

async def run_thread_aio():
    global response_200
    global response_429
    format = "%(asctime)s: %(message)s"
    def send_request():
        asyncio.run(request_aio())
    while True:
        response_200 = 0
        response_429 = 0
        for item in range(1,60):
            x = threading.Thread(target=send_request)
            x.start()
        await asyncio.sleep(1)


async def run_thread_raw():

    global response_200
    global response_429
    format = "%(asctime)s: %(message)s"
    while True:
        response_200 = 0
        response_429 = 0
        for item in range(1,60):
            x = threading.Thread(target=send_request_raw)
            x.start()
        await asyncio.sleep(2)
        
        
async def main_async():
    # run the example with the request object of python
    # await run_thread_raw()
    # Run the example with the library aioHttp
    await run_thread_aio()

asyncio.run(main_async())

  