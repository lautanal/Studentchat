from db import db
import users, admins

# Viestin sisällön haku
def read_message(message_id):
    sql = "SELECT content FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()[0]

# Viestin kirjoittajan id:n haku
def get_user_id(message_id):
    sql = "SELECT user_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()[0]

# Viestin ketjun id:n haku
def get_topic_id(message_id):
    sql = "SELECT topic_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()[0]

# Ketjun viestien haku
def get_messages(topic_id):
    sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message FROM messages M, users U WHERE M.visible = true AND M.topic_id=:topic_id AND M.user_id=U.id ORDER BY M.id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

# Viestien haku tietojen perusteella
def find_messages(user_alias, topic, content):
    user_alias = "%" + user_alias + "%"
    content = "%" + content + "%"
    topic = "%" + topic + "%"
    if user_alias == "" and topic == "":
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message, T.topicname FROM messages M, users U, topics T " \
            "WHERE M.visible = true AND M.user_id=U.id AND M.topic_id=T.id " \
            "AND LOWER(M.content) LIKE LOWER(:content) ORDER BY M.id"
        result = db.session.execute(sql, {"content":content})
    elif content == "" and topic == "":
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message, T.topicname FROM messages M, users U, topics T " \
            "WHERE M.visible = true AND M.user_id=U.id AND M.topic_id=T.id " \
            "AND LOWER(U.alias) LIKE LOWER(:user_alias) ORDER BY M.id"
        result = db.session.execute(sql, {"user_alias":user_alias})
    elif content == "" and user_alias == "":
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message, T.topicname FROM messages M, users U, topics T " \
            "WHERE M.visible = true AND M.user_id=U.id AND M.topic_id=T.id " \
            "AND LOWER(T.topicname) LIKE LOWER(:topic) ORDER BY M.id"
        result = db.session.execute(sql, {"topic":topic})
    elif topic == "":
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message, T.topicname FROM messages M, users U, topics T "\
            "WHERE M.visible = true AND M.user_id=U.id AND M.topic_id=T.id " \
            "AND LOWER(M.content) LIKE LOWER(:content) AND LOWER(U.alias) LIKE LOWER(:user_alias) ORDER BY M.id"
        result = db.session.execute(sql, {"content":content, "user_alias":user_alias})
    elif user_alias == "":
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message, T.topicname FROM messages M, users U, topics T "\
            "WHERE M.visible = true AND M.user_id=U.id AND M.topic_id=T.id " \
            "AND LOWER(M.content) LIKE LOWER(:content) AND LOWER(T.topicname) LIKE LOWER(:topic) ORDER BY M.id"
        result = db.session.execute(sql, {"topic":topic, "content":content})
    elif content == "":
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message, T.topicname FROM messages M, users U, topics T "\
            "WHERE M.visible = true AND M.user_id=U.id AND M.topic_id=T.id " \
            "AND LOWER(U.alias) LIKE LOWER(:user_alias) AND LOWER(T.topicname) LIKE LOWER(:topic) ORDER BY M.id"
        result = db.session.execute(sql, {"user_alias":user_alias, "topic":topic})
    else:
        sql = "SELECT M.id, M.content, U.id, U.alias, M.sent_at, M.ref_message, T.topicname FROM messages M, users U, topics T "\
            "WHERE M.visible = true AND M.user_id=U.id AND M.topic_id=T.id " \
            "AND LOWER(U.alias) LIKE LOWER(:user_alias) AND LOWER(M.content) LIKE LOWER(:content) AND LOWER(T.topicname) LIKE LOWER(:topic) ORDER BY M.id"
        result = db.session.execute(sql, {"user_alias":user_alias, "content":content, "topic":topic})
    return result.fetchall()

# Uuden viestin talletus tietokantaan
def insert(topic_id, content, ref_msg):
    login_id = users.login_id()
    if login_id == 0:
        return False
    sql = "INSERT INTO messages (content, topic_id, user_id, sent_at, visible, ref_message) VALUES (:content, :topic_id, :user_id, NOW(), true, :ref_msg)"
    db.session.execute(sql, {"content":content, "topic_id":topic_id, "user_id":login_id, "ref_msg":ref_msg})
    db.session.commit()
    return True

# Viestin poistaminen (näkyviltä)
def delete(message_id):
    login_id = users.login_id()
    if login_id == 0:
        return False
    sql = "UPDATE messages SET visible = false WHERE id = :message_id"
#    sql = "DELETE FROM messages WHERE id=:message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

# Muutetun viestin talletus tietokantaan
def update(message_id, content):
    login_id = users.login_id()
    if login_id == 0:
        return False
    sql = "UPDATE messages SET CONTENT = :content WHERE id = :message_id"
    db.session.execute(sql, {"content":content, "message_id":message_id})
    db.session.commit()
    return True

# Viestin poistaminen (administraattori)
def admin_delete(message_id):
    admin_id = admins.admin_id()
    if admin_id == 0:
        return False
    sql = "UPDATE messages SET visible = false WHERE id = :message_id"
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True

