import json

import elasticsearch
import asyncio

# docker run --name elastic --network porta -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.10.0

search = elasticsearch.Elasticsearch("http://elastic:9200")


async def elastic_run(pool) -> bool:
    print(search.info())
    if not search.indices.exists(index="textsearch"):
        search.indices.create(index="textsearch",
                              mappings={
                                  "properties": {
                                      "text": {"type": "text"},
                                      "rubrics": {"type": "keyword"}
                                  }
                              }
                              )

    async with pool.acquire() as conn:
        transfer = await conn.fetch("SELECT id, text, rubrics FROM text")

        for row in transfer:
            dict = {"text": row["text"], "rubrics": json.loads(row["rubrics"])}
            print(dict)
            search.index(index="textsearch", id=row["id"], document=dict)

    return True

