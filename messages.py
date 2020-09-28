from db import db
import users, admins

# Viestin sisällön haku
def read_message(message_id):
    sql = "SELECT content FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()[0]

# Viestin kirjoittajan id:n haku
def get_author(message_id):
    sql = "SELECT user_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()[0]

# Ketjun viestien haku
def get_messages(topic_id):
    sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at FROM messages M, users U WHERE visible = true AND M.topic_id=:topic_id AND M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

# Uuden viestin talletus tietokantaan
def insert(topic_id, content, reply_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO messages (content, topic_id, user_id, sent_at, reply_id, visible) VALUES (:content, :topic_id, :user_id, NOW(), :reply_id, true)"
    db.session.execute(sql, {"content":content, "topic_id":topic_id, "user_id":user_id, "reply_id":reply_id})
    db.session.commit()
    return True

# Viestin poistaminen (näkyviltä)
def delete(message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE messages SET visible = false WHERE id = :message_id"
#    sql = "DELETE FROM messages WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

# Muutetun viestin talletus tietokantaan
def update(message_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE messages SET CONTENT = :content WHERE id = :message_id"
    db.session.execute(sql, {"content":content, "message_id":message_id})
    db.session.commit()
    return True

# Viestin poistaminen (admin)
def admin_delete(message_id):
    admin_id = admins.admin_id()
    if admin_id == 0:
        return False
    sql = "DELETE FROM messages WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

