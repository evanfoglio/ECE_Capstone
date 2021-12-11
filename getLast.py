#!/usr/bin/python3
import sqlite3
def get_last(db, data):

        try:
                sqlcon = sqlite3.connect(db)
                cursor = sqlcon.cursor()
        except sqlite3.Error as error:
                print("ERROR, ", error)

        finally:
                if sqlcon:
                        cursor.execute("select " + data + " from data order by datetime desc limit 1;")
                        last_val = cursor.fetchall()
                        cursor.close()
                        sqlcon.close()
                        return last_val

