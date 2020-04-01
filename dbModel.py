# _*_ coding: utf-8 _*_
# jetDm code
from peewee import *
from playhouse.sqlite_ext import *
import peewee
import datetime

# Подключение к БД с учетом расширения FTS
lib_db = SqliteExtDatabase('db/Lib.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 32})


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


# Дополнительная модель Таблицы для полнотекстового поиска в Функции add_to_lib запись добавляется с учетом этой таблицы
class FTSLibrary(FTSModel):
    name = TextField()

    class Meta:
        database = lib_db


# Добавление категории
# :TODO переделать надо
def add_category(name):
    row = Category(
        name=name.lower().strip(),
    )
    row.save()


# функция добавления записи в библиотеку
def add_to_lib(name, url, category):
    library = Library.create(
        name=name,
        url=url,
        category=category
    )
    FTSLibrary.create(
        docid=library.id,
        name='\n'.join((library.name, library.url))
    )


# :TODO переделать надо
# def add_to_lib(name, url, category):
#     cat_exist = True
#     try:
#         category = Library.select().where(Library.name == name.strip()).get()
#     except DoesNotExist as de:
#         cat_exist = False
#
#     if cat_exist:
#         row = Library(
#             name=name.lower().strip(),
#             url=url,
#             category=category
#         )
#         row.save()

# :TODO Этим тестил

# Искать можно по MATCH '<word1> AND <WORD2> OR <word3>'

# SELECT Library.name,Library.url, Library.category_id
# FROM Library
# JOIN FTSLibrary ON Library.id = ftslibrary.docid
# WHERE ftslibrary MATCH 'new item'

# dbModel.add_to_lib('Newless one sites','newy irls',1)
# dbModel.add_to_lib('New less one sites','newy irls',1)
# dbModel.add_to_lib('new less one sites','newy irls',1)
# dbModel.add_to_lib('new2 less ones sits','new ssy irls',1)
# dbModel.add_to_lib('newcc lesees ones sits','new1 ssy irls',1)
# dbModel.add_to_lib('newcc lesees onesssss sits','new ssy irls',1)

if __name__ == '__main__':
    try:
        lib_db.connect()
        Library.create_table()
        FTSLibrary.create_table()
    except peewee.InternalError as px:
        print(str(px))
    try:
        Category.create_table()
    except peewee.InternalError as px:
        print(str(px))
