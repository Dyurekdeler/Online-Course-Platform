from OnlineCoursePlatform.settings import DATABASES
from dbconnector.connector import Postgresql, Query

def open_connection_to_db():
    resultdb = DATABASES.get('default')
    db = Postgresql(    host    = resultdb.get('HOST'),
                        port    = resultdb.get('PORT'),
                        db      = resultdb.get('NAME'),
                        user    = resultdb.get('USER'),
                        passwd  = resultdb.get('PASSWORD'))

    return db

def get_from_db(query):
    db          = open_connection_to_db()
    cursor      = db.connection()
    querycursor = Query(cursor)
    return querycursor.run(query)

def update_db(query):
    db          = open_connection_to_db()
    cursor      = db.connection()
    querycursor = Query(cursor)
    return querycursor.update(query)

def insert_db(query):
    db          = open_connection_to_db()
    cursor      = db.connection()
    querycursor = Query(cursor)
    return querycursor.insert(query)

def call_proc(query):
    db = open_connection_to_db()
    cursor = db.connection()
    querycursor = Query(cursor)
    return querycursor.callproc(query)