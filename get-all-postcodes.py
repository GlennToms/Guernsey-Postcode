from re import I
import requests
import string
import asyncio
import aiohttp
import time
import json


def geturl(postcode):
    url = f"https://guernsey.isl-fusion.com/api/search/{postcode}"

    proxies = {"http": "http://localhost:8080"}
    # r = requests.get(url, proxies=proxies)
    r = requests.get(url)
    return r


def gen_postcode():
    run = True
    while run:
        for number_one in range(1, 11):
            for number_two in range(10):
                for first_letter in string.ascii_uppercase:
                    for second_letter in string.ascii_uppercase:
                        yield f"GY{number_one} {number_two}{first_letter}{second_letter}"
        run = False


def write(name, data):
    if data.get("results"):
        with open(f"{name}.json", "w") as outfile:
            outfile.write(json.dumps(data.get("results"), indent=4))


async def by_aiohttp():
    async with aiohttp.ClientSession() as session:
        url = "https://guernsey.isl-fusion.com/api/search/"

        for postcode in gen_postcode():
            res = await session.get(url + postcode)
            # res = await session.get("https://guernsey.isl-fusion.com/api/search/GY1 1AH")
            print(postcode)
            if res.status == 200:
                write(name=postcode, data=await res.json())


start_time = time.time()
asyncio.run(by_aiohttp())
print("--- It took %s seconds ---" % (time.time() - start_time))
