from peewee import PostgresqlDatabase, Model, TextField, AutoField
import csv
# docker run -d --name porta --network porta -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=porta -p 5432:5432 postgres:15
bd = PostgresqlDatabase(
    "porta",
    user="admin",
    password="admin",
    host="porta",
    port=5432
)

class Text(Model):
    class Meta:
        database = bd
    id = AutoField(primary_key=True)
    rubrics = TextField()
    text = TextField()
    created_date = TextField()





def bd_activate():
    #Создаём базу
    bd.connect()
    bd.create_tables(Model.__subclasses__())
    #Переносим данные из ксв
    with open("posts.csv", encoding="UTF-8") as file:
        read = csv.reader(file)
        for line in read:
            Text.create(rubrics=line[2], text=line[0], created_date=line[1])

    test = Text.get(Text.id == 34)
    print(test.created_date, test.text)







