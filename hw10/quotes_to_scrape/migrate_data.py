import os
import django
from pymongo import MongoClient
from hw10.quotes_to_scrape.models import Author, Quote  # Обновленный импорт

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10.settings")  # Обновленное значение

django.setup()

def migrate_data():
    # Подключение к MongoDB
    mongo_client = MongoClient("mongodb+srv://vrokmoitcattus:owtXMbGQIFr2444j@hw8.3qphtkz.mongodb.net/celebrities?retryWrites=true&w=majority")
    mongo_db = mongo_client.celebrities

    # Извлечение данных из MongoDB и сохранение их в PostgreSQL
    for author_data in mongo_db.author.find():
        author = Author.objects.create(
            fullname=author_data['fullname'],
            born_date=author_data.get('born_date'),
            born_location=author_data.get('born_location'),
            description=author_data.get('description')
        )
        for quote_data in mongo_db.quote.find({'author_id': author_data['_id']}):
            Quote.objects.create(
                author=author,
                text=quote_data['text'],
                tags=quote_data.get('tags', [])
            )

if __name__ == "__main__":
    migrate_data()
