# _*_ coding: utf-8 _*_
# jetDm code
import sqlite3
from botSetting import database

def get_category():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('select * from category')
    themes = {}
    for i in cursor.fetchall():
        themes[i[0]] = i[1]
    conn.close()
    return themes
