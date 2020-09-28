from db import db

# Alueen viestiketjujen haku
def get_topics(area_id):
    sql = "SELECT id, topicname, area_id FROM topics WHERE area_id=:area_id ORDER BY id"
    result = db.session.execute(sql, {"area_id":area_id})
    return result.fetchall()

def get_topicname(topic_id):
    sql = "SELECT topicname FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchone()[0]


#U uden viestiketjun talletus tietokantaan
def sendtopic(area_id, topic_name):
#    user_id = users.user_id()
#    if user_id == 0:
#        return False
    sql = "INSERT INTO topics (topicname, area_id) VALUES (:topic_name, :area_id)"
    db.session.execute(sql, {"topic_name":topic_name, "area_id":area_id})
    db.session.commit()
    return True
