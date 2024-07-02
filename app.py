from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from dotenv import dotenv_values

from models import Pokemon

config = dotenv_values('.env')

USER = config.get('USER')
PASSWORD = config.get('PASSWORD')
DB = config.get('DB')
HOST = config.get('HOST')

DB_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB}'

ENGINE = create_engine(DB_URL)

LOCAL_SESSION = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False)

app = FastAPI(
    openapi_tags=[
        {
            'name': 'v1',
            'description': 'Version 1.0'
        }
    ]
)

templates = Jinja2Templates(directory='templates')


def get_database():
    db = LOCAL_SESSION()
    try:
        yield db
    finally:
        db.close()


@app.get('/api/v1/pokemons', response_class=HTMLResponse, tags=['v1'])
async def get_pokemon(request: Request, db: Session = Depends(get_database)):
    pokemon_list = db.query(Pokemon).all()
    context = {
        'request': request,
        'pokemon_list': pokemon_list,
        'post_url': '/api/v1/pokemons'
    }
    return templates.TemplateResponse('pokemon.html', context)


@app.post('/api/v1/pokemons', response_class=HTMLResponse, tags=['v1'])
async def filter_pokemon(request: Request,
                         name: str = Form(None),
                         types: str = Form(None),
                         db: Session = Depends(get_database)):
    pokemon_filter = db.query(Pokemon)

    filters = []
    if name:
        filters.append(Pokemon.name.ilike(f'%{name}%'))
    if types:
        filters.append(Pokemon.types.ilike(f'%{types}%'))

    if filters:
        pokemon_filter = pokemon_filter.filter(or_(*filters))

    pokemon_list = pokemon_filter.all()

    context = {
        'request': request,
        'pokemon_list': pokemon_list,
        'post_url': '/api/v1/pokemons'
    }
    return templates.TemplateResponse('pokemon.html', context)