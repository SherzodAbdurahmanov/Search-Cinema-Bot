from peewee import SqliteDatabase, Model, IntegerField, CharField, DateTimeField
import datetime

db = SqliteDatabase('movie_bot.db')


class BaseModel(Model):
    class Meta:
        database = db


class SearchHistory(BaseModel):
    user_id = IntegerField()
    query_type = CharField()  # Например, 'title', 'rating', 'low_budget', 'high_budget'
    query_value = CharField()  # Сохранение значений запроса
    timestamp = DateTimeField(default=datetime.datetime.now)


