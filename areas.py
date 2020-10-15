from db import db
import admins

# Keskustelualueiden haku (käyttöoikeuksien mukaan)
def get_areas(user_rights):
    if (user_rights > 1):
        sql = "SELECT id, areaname FROM areas WHERE locked != true ORDER BY id"
    else:
        sql = "SELECT id, areaname FROM areas WHERE locked != true AND hidden = false ORDER BY id"
    result = db.session.execute(sql, {"user_rights":user_rights})
    return result.fetchall()

# Keskustelualueiden haku (kaikki)
def get_areas_all():
    sql = "SELECT id, areaname, hidden, locked FROM areas ORDER BY id"
    result = db.session.execute(sql)
    return result.fetchall()

# Keskustelualueen nimi
def get_areaname(area_id):
    sql = "SELECT areaname FROM areas WHERE id = :area_id"
    result = db.session.execute(sql, {"area_id":area_id})
    return result.fetchone()[0]

# Uuden viestiketjunkeskustelualueen talletus tietokantaan
def sendarea(area_name, hidden, locked):
    admin_id = admins.admin_id()
    if admin_id == 0:
        return False
    if (hidden == "0"):
        sql = "INSERT INTO areas (areaname, hidden, locked) VALUES (:area_name, false, false)"
    else:
        sql = "INSERT INTO areas (areaname, hidden, locked) VALUES (:area_name, true, false)"
    db.session.execute(sql, {"area_name":area_name})
    db.session.commit()
    return True

