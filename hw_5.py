import sys

import aiohttp
import asyncio
import platform



class HttpError(Exception):
    pass


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
            raise HttpError(f'Connection error: {url}', str(err))


async def main(index_day):
    date = datetime.now - timedelta(days=2)
    try:
        response = await request('https://api.privatbank.ua/p24api/exchange_rates?date=01.12.2014')
        return response
    except HttpError as err:
        print(err)
        return None


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(sys.argv)
    r = asyncio.run(main(sys.argv[2]))
    print(r)
