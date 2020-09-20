from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

#Login
def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            return True
        else:
            return False

#Logout
def logout():
    del session["user_id"]

#Uusi käyttäjä
def register(username,password,alias):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,privileges,alias) VALUES (:username,:password,0,:alias)"
        db.session.execute(sql, {"username":username,"password":hash_value,"alias":alias})
        db.session.commit()
    except:
        return False
    return login(username,password)

def user_id():
    return session.get("user_id",0)

def get_username():
    user_id = session.get("user_id",0)
    sql = "SELECT username FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def get_useralias():
    user_id = session.get("user_id",0)
    sql = "SELECT alias FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def get_userrights():
    user_id = session.get("user_id",0)
    sql = "SELECT privileges FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]
