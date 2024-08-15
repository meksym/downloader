import logging
from aiohttp import ClientSession


async def post(url: str, data: dict, session: ClientSession) -> dict:
    response = await session.post(url, json=data)

    try:
        return await response.json()
    except Exception as e:
        logging.critical(
            f'Excetion: {e}\n'
            f'URL: {url}\n'
            f'Content: %s' % await response.text()
        )
        raise e


async def get(url: str, session: ClientSession) -> bytes:
    response = await session.get(url)
    return await response.read()
