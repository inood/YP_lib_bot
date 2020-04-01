# _*_ coding: utf-8 _*_
# jetDm code
from peewee import *
import peewee
import datetime

lib_db = SqliteDatabase('db/Lib.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class BaseModel(Model):
    class Meta:
        database = lib_db


class Category(BaseModel):
    id = PrimaryKeyField(null=False)
    name = TextField()

    class Meta:
        db_table = "Category"
        order_by = ('id',)

class Library(BaseModel):
    id = PrimaryKeyField(null=False)
    name = TextField()
    url = TextField()
    category = ForeignKeyField(Category, related_name='fk_cat_lib', to_field='id', on_delete='cascade',
                               on_update='cascade')
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "Library"
        order_by = ('id',)


def add_to_lib(name, url, category):
    cat_exist = True
    try:
        category = Library.select().where(Library.name == name.strip()).get()
    except DoesNotExist as de:
        cat_exist = False

    if cat_exist:
        row = Library(
            name=name.lower().strip(),
            url=url,
            category=category
        )
        row.save()

if __name__ == '__main__':
    try:
        lib_db.connect()
        Library.create_table()
    except peewee.InternalError as px:
        print(str(px))
    try:
        Category.create_table()
    except peewee.InternalError as px:
        print(str(px))
