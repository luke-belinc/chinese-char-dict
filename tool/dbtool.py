import os
import datetime
from . import initialize

# annoying workaround for 'file not found' error
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

class DBTool(object):
    psql_connect = initialize.begin()
    initialized = 1 #if psql_connect is not -1 else 0

    # method to get connected to the database
    @classmethod
    def get_connected(cls, dbHost='localhost', dbName='dictionary', dbUser='postgres', dbPass='postgres'):
        try:
            if (cls.initialized):
                cls.conn = cls.psql_connect(host=dbHost, database=dbName, user=dbUser, password=dbPass)
                cls.write_log(cls, "obtained connection successfully")
            else:
                raise Exception("database not initalized!")
        except Exception as err:
            cls.write_log(cls, str(err))

    # method to get cursor
    @classmethod
    def get_cursor(cls):
        if cls.conn is not None:
            cls.curs = cls.conn.cursor()
            cls.write_log(cls, "obtained cursor successfully")
        else:
            cls.write_log(cls, "psql connect object is not initialized")


    @classmethod
    def close_connection(cls):
        cls.write_log(cls, "Closing connection and cursor if they're open...")
        if (cls.conn != None):
            cls.conn.close()
        if (cls.curs != None):
            cls.curs.close()

        cls.curs = None
        cls.conn = None


# class UserTable(DBTool):
#     log = open(os.path.join(THIS_FOLDER, 'logs', 'usertable.log'), 'a+', encoding='utf-8')
#     conn = None
#     curs = None

#     def __init__(self, *args):
#         self.get_connected()
#         self.get_cursor()
#         if (self.curs is not None):
#             self.execute = self.curs.execute

#             self.write_log("checking for usertable...")
#             self.execute("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename=\'usertable\');")
#             if (self.curs.fetchone()[0] is False):
#                 self.write_log("attempting to create user table...")
#                 self.execute("CREATE TABLE usertable (id SERIAL PRIMARY KEY, entry TEXT UNIQUE NOT NULL, defin TEXT)")
#                 self.conn.commit()
#             else:
#                 self.write_log("table already exists...")

#     def add_row(self, entry='', defin=''):
#         if (entry is not ''):
#             self.write_log("adding " + entry + " to the usertable...")
#             self.execute()
#             self.curs.commit()

#     def write_log(self, msg):
#         t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         line = '[' + t + '] -> ' + str(msg) + '\n'
#         self.log.write(line)
        
class CharTable(DBTool):
    log = open(os.path.join(THIS_FOLDER, 'logs', 'chartable.log'), 'a+', encoding='utf-8')
    conn = None
    curs = None

    def __init__(self, name='characters'):
        self.get_connected()
        self.get_cursor()
        if self.curs is not None:
            self.execute = self.curs.execute

    def get_character_data(self, char=None, col=None):
        if (char != None):
            uid = ord(char)
            self.curs.execute("SELECT definition FROM characters c WHERE c.unicode=" + str(uid))
            definition = str(self.curs.fetchone()[0])
            self.curs.execute("SELECT pinyin FROM characters c WHERE c.unicode=" + str(uid))
            pinyin = str(self.curs.fetchone()[0][0])
            return (definition,pinyin)

    def write_log(self, msg):
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = '[' + t + '] -> ' + str(msg) + '\n'
        self.log.write(line)