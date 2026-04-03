import csv
import asyncio
import json
# docker run -d --name porta --network porta -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=porta -p 5432:5432 postgres:15



async def bd_activate(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS text (
                id SERIAL PRIMARY KEY,
                rubrics JSONB,
                text TEXT,
                created_date TEXT
            )
        """)

        with open("posts.csv", encoding="UTF-8") as file:
            read = csv.reader(file)
            for line in read:
                rubrics_str = line[2].strip()
                if rubrics_str.startswith("[") and rubrics_str.endswith("]"):
                    rubrics_str = rubrics_str[1:-1]
                rubrics_list = [x.strip().strip("'\"") for x in rubrics_str.split(",")]
                rubrics_json = json.dumps(rubrics_list)
                await conn.execute(
                    "INSERT INTO text (rubrics, text, created_date) VALUES ($1, $2, $3)",
                    rubrics_json, line[0], line[1]
            )










