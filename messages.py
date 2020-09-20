from db import db
import users

#Viestin haku
def read_message(id):
    sql = "SELECT content FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

#Ketjun viestien haku
def get_messages(topic_id):
    sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at FROM messages M, users U WHERE M.topic_id=:topic_id AND M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

#Uuden viestin talletus tietokantaan
def send(topic_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, topic_id, user_id, sent_at) VALUES (:content, :topic_id, :user_id, NOW())"
    db.session.execute(sql, {"content":content, "topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return True

#Viestin poistaminen
def delete(id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "DELETE FROM messages WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True

#Muutetun viestin talletus tietokantaan
def modify(message_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE messages SET CONTENT = :content WHERE id = :id"
    db.session.execute(sql, {"content":content, "id":message_id})
    db.session.commit()
    return True
