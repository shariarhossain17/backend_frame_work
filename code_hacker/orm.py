
import sqlite3
class Database:
    def __init__(self,path):
        self.conn=sqlite3.Connection(path)

    @property
    def tables(self):
        return []   
    


class Table:
    pass

class Column:
    def __init__(self, column_type):
        self.type = column_type

    @property
    def sql_type(self):
        SQLITE_TYPE_MAP = {
            int: "INTEGER",
            float: "REAL",
            str: "TEXT",
            bytes: "BLOB",
            bool: "INTEGER",  # 0 or 1
        }
        return SQLITE_TYPE_MAP[self.type]



class ForeignKey:
    def __init__(self, table):
        self.table = table