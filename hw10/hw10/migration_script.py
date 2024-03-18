import pymongo
import psycopg2
from psycopg2 import sql

# Підключення до MongoDB
mongo_client = pymongo.MongoClient("mongodb+srv://vrokmoitcattus:owtXMbGQIFr2444j@hw8.3qphtkz.mongodb.net/celebrities?retryWrites=true&w=majority")
mongo_db = mongo_client["celebrities"]

# Підключення до PostgreSQL
postgres_conn = psycopg2.connect(
    dbname="myquotesapp",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
postgres_cur = postgres_conn.cursor()

def migrate_data():
    # Отримання даних з MongoDB та збереження їх у PostgreSQL
    for author_data in mongo_db.author.find():
        postgres_cur.execute("""
            INSERT INTO author (fullname, born_date, born_location, description)
            VALUES (%s, %s, %s, %s)
        """, (author_data['fullname'], author_data.get('born_date'), author_data.get('born_location'), author_data.get('description')))
        author_id = postgres_cur.lastrowid

        for quote_data in mongo_db.quote.find({'author': author_data['_id']}):
            postgres_cur.execute("""
                INSERT INTO quote (author_id, text)
                VALUES (%s, %s)
            """, (author_id, quote_data['quote']))
            quote_id = postgres_cur.lastrowid

            for tag_name in quote_data['tags']:
                postgres_cur.execute("""
                    INSERT INTO tag (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                """, (tag_name,))
                postgres_cur.execute("""
                    SELECT id FROM tag WHERE name = %s
                """, (tag_name,))
                tag_id = postgres_cur.fetchone()[0]

                postgres_cur.execute("""
                    INSERT INTO quote_tag (quote_id, tag_id)
                    VALUES (%s, %s)
                """, (quote_id, tag_id))

    # Завершення транзакції та збереження змін у PostgreSQL
    postgres_conn.commit()

# Виклик функції для міграції даних
migrate_data()

# Закриття з'єднань
mongo_client.close()
postgres_cur.close()
postgres_conn.close()
