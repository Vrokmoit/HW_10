import pymongo
import psycopg2

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

def add_mongo_id_to_author():
    for author_data in mongo_db.author.find():
        # Додавання поля 'mongo_id' до таблиці 'author' у PostgreSQL
        # Конвертуємо ObjectId у строку
        mongo_id_str = str(author_data['_id'])
        postgres_cur.execute("""
            UPDATE author 
            SET mongo_id = %s 
            WHERE mongo_id = %s
        """, (mongo_id_str, mongo_id_str))
    # Збереження змін у PostgreSQL
    postgres_conn.commit()

# Виклик функції для додавання поля 'mongo_id' до таблиці 'author'
add_mongo_id_to_author()

# Закриття з'єднань
mongo_client.close()
postgres_cur.close()
postgres_conn.close()
