import sys
from datetime import datetime, timedelta

import aiohttp
import asyncio
import platform


class HttpError(Exception):
    pass


async def request(url):
    async with aiohttp.ClientSession() as client:
        try:
            async with client.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {r.status} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
            raise HttpError(f"Error connecting to {url}, {str(err)}")


async def main(index_day):
    try:
        index_day = int(index_day)
        if index_day < 0 or index_day > 10:
            print("Index day must be between 0 and 10")
            return None
    except ValueError:
        print("Index day must be an integer")
        return None
    date = datetime.now() - timedelta(days=int(index_day))
    shift = date.strftime("%d.%m.%Y")

    try:
        response = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={shift}')
        return response
    except HttpError as err:
        print(err)
        return None


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(sys.argv)
    r = asyncio.run(main(sys.argv[1]))
    print(r)
