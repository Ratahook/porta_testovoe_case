from elasticsearch import NotFoundError
from bd import Text
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    rubrics: str
    text: str
    created_date: str

def searcher(search, call_text):
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

    for i, elem in enumerate(results):
        id = elem['id']
        bd_odj = Text.get(Text.id == id)
        results[i] = Item(id=bd_odj.id, rubrics=bd_odj.rubrics, text=bd_odj.text, created_date=bd_odj.created_date)

    results.sort(key=lambda x: x.created_date)

    final  = [item.model_dump() for item in results]
    return final

def delete_by_id(es, model, doc_id):
    deleted = model.delete().where(model.id == doc_id).execute()
    try:
        es.delete(index="textsearch", id=doc_id)
    except NotFoundError:
        pass
    return deleted
