import json
from elasticsearch import NotFoundError
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    rubrics: list
    text: str
    created_date: str

async def get_by_id(pool, search, doc_id: int) -> Item:
    response = search.get(
        index="textsearch",
        id=doc_id
    )

    id = int(response["_id"])

    async with pool.acquire() as conn:
        data = await conn.fetchrow(
            "SELECT * FROM text WHERE id = $1",
            id
        )

    results = Item(id=data["id"], rubrics=json.loads(data["rubrics"]), text=data["text"], created_date=data["created_date"])

    return results

async def searcher(pool, search, call_text: str) -> List[Item]:
    response = search.search(
        index="textsearch",
        query={
            "match":{
                "text": call_text
            }
        },
        size=20
    )

    results = []
    for hit in response["hits"]["hits"]:
        results.append({
            "id": hit["_id"],
        })


    async with pool.acquire() as conn:
        for i, elem in enumerate(results):
            id = int(elem['id'])
            row = await conn.fetchrow(
                "SELECT * FROM text WHERE id = $1",
                id
            )
            results[i] = Item(id=row["id"], rubrics=json.loads(row["rubrics"]), text=row["text"], created_date=row["created_date"])

    results.sort(key=lambda x: x.created_date)

    return results

# МЕТОД НЕ РАБОТАЕТ
async def searcher_rubrics(pool, search, call_rub: str) -> List[Item]:
    response = search.search(
        index="textsearch",
        query={
            "term": {
                "rubrics": call_rub
            }
        },
        size=20
    )
    results = []
    for hit in response["hits"]["hits"]:
        results.append({
            "id": hit["_id"],
        })

    async with pool.acquire() as conn:
        for i, elem in enumerate(results):
            id = int(elem['id'])
            row = await conn.fetchrow(
                "SELECT * FROM text WHERE id = $1",
                id
            )
            results[i] = Item(id=row["id"], rubrics=json.loads(row["rubrics"]), text=row["text"], created_date=row["created_date"])


    results.sort(key=lambda x: x.created_date)

    return results

async def delete_by_id(pool, es, doc_id: int):
    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                row = await conn.fetchrow(
                    "SELECT * FROM text WHERE id = $1",
                    doc_id
                )
                if not row:
                    return "DELETE 0"

                deleted = await conn.execute(
                    "DELETE FROM text WHERE id = $1",
                    doc_id
                )
                if deleted == "DELETE 0":
                    return deleted
                try:
                    es.delete(index="textsearch", id=doc_id)
                except NotFoundError:
                    pass
                except Exception as e:
                    await conn.execute(
                        "INSERT INTO text (id, rubrics, text, created_date) VALUES ($1, $2, $3, $4)",
                        row["id"], row["rubrics"], row["text"], row["created_date"]
                    )
                    raise
        return deleted
    except Exception as e:
        return f"DB error: {e}"


