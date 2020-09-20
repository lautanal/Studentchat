from db import db

#Viestialueiden haku
def get_areas(user_rights):
    sql = "SELECT id, areaname FROM areas WHERE hidden <= :user_rights ORDER BY id"
    result = db.session.execute(sql, {"user_rights":user_rights})
    return result.fetchall()

def get_areaname(area_id):
    sql = "SELECT areaname FROM areas WHERE id = :area_id"
    result = db.session.execute(sql, {"area_id":area_id})
    return result.fetchone()[0]
