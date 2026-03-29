# Porta_testovoe_case


## Стек

- Python
- PostgreSQL
- Elasticsearch
- Docker

### Запуск

- docker network create porta
- docker run --name elastic --network porta -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.10.0
- docker run -d --name porta --network porta -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=porta -p 5432:5432 postgres:15
- docker build -t porta_app .
- docker run -p 8000:8000 --network porta porta_app
