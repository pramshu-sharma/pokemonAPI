from aiohttp.client_exceptions import ContentTypeError
from typing import Dict, Any
from dotenv import dotenv_values

import asyncpg, aiohttp, asyncio

config = dotenv_values('.env')

API_ENDPOINT = config.get('API_ENDPOINT')
USER = config.get('USER')
PASSWORD = config.get('PASSWORD')
DB = config.get('DB')
HOST = config.get('HOST')


async def fetch_data(url: str) -> Dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return {
                'pokedex': data['id'],
                'name': data['name'].capitalize(),
                'image': data['sprites']['other']['official-artwork']['front_default'],
                'types': ', '.join([data['types'][num]['type']['name'].capitalize() for num in range(len(data['types']))])
            }


async def load_data(data: Dict[str, Any]):
    conn = await asyncpg.connect(
        user=USER,
        password=PASSWORD,
        database=DB,
        host=HOST
    )

    create_query = """
        CREATE TABLE IF NOT EXISTS pokemon (
            pokedex INT PRIMARY KEY,
            name TEXT NOT NULL,
            image TEXT NOT NULL,
            types TEXT NOT NULL
        )
    """

    insert_query = """
        INSERT INTO pokemon (pokedex, name, image, types)
        VALUES ($1, $2, $3, $4)
    """

    async with conn.transaction():
        await conn.execute(create_query)
        await conn.execute(insert_query, data['pokedex'], data['name'], data['image'], data['types'])

    await conn.close()


async def main():
    current_pokemon = 1
    while True:
        try:
            url = f'{API_ENDPOINT}{current_pokemon}'
            pokemon = await fetch_data(url)
            print(f'INSERTING DATA FOR POKEMON ID: {current_pokemon}')
            await load_data(pokemon)
        except ContentTypeError:
            break
        except Exception as e:
            print(f'Error Processing Pokemon ID {current_pokemon}: {e}')
        current_pokemon += 1


asyncio.run(main())
