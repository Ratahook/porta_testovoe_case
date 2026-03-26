
import json
from fastapi import FastAPI
from elasticsearch import Elasticsearch
from handlers import searcher, delete_by_id
from bd import Text, bd_activate
from elastic import elastic_run

app = FastAPI()
search = Elasticsearch("http://elastic:9200")

# docker network create porta
# docker build -t porta_app .
# docker run -p 8000:8000 --network porta porta_app

@app.get("/boot")
def app_boot():
    bd_activate()
    if elastic_run():
        return f'Запуск успешно выполнен'

@app.get("/search")
def app_search(text: str):
    return searcher(search, text)

@app.get("/del")
def app_delete(id: int):
    res = delete_by_id(search, Text, id)
    print(res)
    if res == '1':
        return f'Текстовый блок с айди {id}, успешно удалён'
    else:
        return f'Текстового блока с айди {id} не существует'

if __name__ == '__main__':
    with open("docs.json", "w", encoding="utf-8") as f:
        json.dump(app.openapi(), f, ensure_ascii=False, indent=2)