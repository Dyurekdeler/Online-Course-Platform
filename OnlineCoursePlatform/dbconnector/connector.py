import psycopg2
import sys

class Postgresql:

    def __init__(self, host, port, db, user, passwd):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.conn_string = self.set_conn_string()

    def set_conn_string(self):
        return "host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (
            self.host, self.port, self.db, self.user, self.passwd)

    def connection(self):
        try:
            self.conn = psycopg2.connect(self.conn_string)
            self.conn.autocommit = True;
            return self.conn.cursor()
        except:
            print ("Database connection failed!\n ->%s" % (sys.exc_info()[1]))
            raise Exception('Database connection failed!')

    def close(self):
        self.conn.close()

    def getDB(self):
        return self.db


class Query:
    def __init__(self, cursor):
        self.cursor = cursor

    def run(self, query):
        try:
            self.cursor.execute(query)
            return 'SUCCESS', self.cursor.fetchall()
        except:
            return 'FAILURE', (sys.exc_info()[1])

    def insert(self, query):
        try:
            self.cursor.execute(query)
            return "SUCCESS"
        except psycopg2.Error as e:
            print( e.pgerror)
            raise Exception(e.pgerror)

    def update(self, query):
        try:
            self.cursor.execute(query)
            return "SUCCESS"
        except:
            raise (sys.exc_info()[1])