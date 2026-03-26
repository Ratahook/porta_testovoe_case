import elasticsearch
from bd import Text

# docker run --name elastic --network porta -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.10.0

search = elasticsearch.Elasticsearch("http://elastic:9200")


def elastic_run():
    print(search.info())
    if not search.indices.exists(index="textsearch"):
        search.indices.create(index="textsearch",
                              mappings={
                                  "properties": {
                                      "text": {"type": "text"}
                                  }
                              }
                              )

    transfer = Text.select(Text.id, Text.text)

    for row in transfer:
        dict = {"text": row.text}
        print(dict)
        search.index(index="textsearch", id=row.id, document=dict)

    return True
