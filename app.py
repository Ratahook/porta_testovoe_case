import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from handlers import searcher, delete_by_id, searcher_rubrics, get_by_id, Item
from bd import bd_activate
from elastic import elastic_run, search
import asyncpg
from config import settings

# Поиск по рубрикам

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    app.state.db_pool = await asyncpg.create_pool(
        database=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port
    )
    await bd_activate(app.state.db_pool)
    await elastic_run(app.state.db_pool)
    yield
    # shutdown
    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

# docker network create porta
# docker run -d --name porta --network porta -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=porta -p 5432:5432 postgres:15
# docker run --name elastic --network porta -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.10.0
# docker build -t porta_app .
# docker run -p 8000:8000 --network porta porta_app
# ["VK-1603736028819866", "VK-56826133514", "VK-60102223342"]


@app.get("/id/{id}", response_model=Item)
async def app_id_get(id: int):
    result = await get_by_id(app.state.db_pool, search, id)
    return result

@app.get("/search", response_model=list[Item])
async def app_search(text: str):
    result = await searcher(app.state.db_pool, search, text)
    return result

# МЕТОД НЕ РАБОТАЕТ
@app.get("/rubric", response_model=list[Item])
async def app_search_rubric(rubric: str):
    result = await searcher_rubrics(app.state.db_pool, search, rubric)
    return result

@app.delete("/del/{id}")
async def app_delete(id: int):
    res = await delete_by_id(app.state.db_pool, search, id)
    print(res)
    if res == 'DELETE 1':
       return f'Текстовый блок с айди {id}, успешно удалён'
    else:
        return f'Текстового блока с айди {id} не существует'

if __name__ == '__main__':
    with open("docs.json", "w", encoding="utf-8") as f:
        json.dump(app.openapi(), f, ensure_ascii=False, indent=2)