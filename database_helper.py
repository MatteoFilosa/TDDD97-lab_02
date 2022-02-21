import sqlite3
from flask import g

DATABASE_URI = 'database.db'


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE_URI)

    return db

def disconnect_db():
    db = getattr(g, 'db', None)

    if db is not None:
        db.close
        g.db = None

def create_user(email, password, firstname, familyname, gender, city, country):
    try:
        get_db().execute("insert into user values(?,?,?,?,?,?,?)", [email, password, firstname, familyname, gender, city, country])

        get_db().commit()
        return True
    except:
        return False



def find_user(email, password):

    cursor = get_db().execute("select * from user where user.email = ? and password = ?", [email, password])
    rows = cursor.fetchall()
    cursor.close()
    print(rows)
    if rows:
        return True
    else:
        return False

def new_password(token, password, newpassword):

    try:
        get_db().execute("update user set password = ? where password = ?", [newpassword,password])
        get_db().commit()
        return True
    except:
        return False
