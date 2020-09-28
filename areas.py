from db import db

# Viestialueiden haku
def get_areas(user_rights):
    if (user_rights > 0):
        sql = "SELECT id, areaname FROM areas ORDER BY id"
    else:
        sql = "SELECT id, areaname FROM areas WHERE hidden = false ORDER BY id"
    result = db.session.execute(sql, {"user_rights":user_rights})
    return result.fetchall()

# Viestialueiden haku (kaikki)
def get_areas_all():
    sql = "SELECT id, areaname, hidden FROM areas ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

def get_areaname(area_id):
    sql = "SELECT areaname FROM areas WHERE id = :area_id"
    result = db.session.execute(sql, {"area_id":area_id})
    return result.fetchone()[0]
