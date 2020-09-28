from app import app
from flask import render_template, request, redirect
import users, areas, topics, messages, admins

@app.route("/admin")
def admin():
    return render_template("adindex.html")

# Viestialueiden hallinta
@app.route("/admin/areas")
def ad_list_areas():
    list = areas.get_areas_all()
    user_name = admins.get_adminname()
    return render_template("adareas.html", user_name=user_name, areas=list)

# Viestiketjujen hallinta
@app.route("/admin/topics/<int:area_id>")
def ad_list_topics(area_id):
    user_name = admins.get_adminname()
    area_name = areas.get_areaname(area_id)
    list = topics.get_topics(area_id)
    return render_template("adtopics.html", user_name=user_name, area_id=area_id, area_name=area_name, topics=list)

# Viestien hallinta
@app.route("/admin/messages/<int:area_id>/<int:topic_id>")
def ad_list_messages(area_id, topic_id):
    user_name = admins.get_adminname()
    area_name = areas.get_areaname(area_id)
    topic_name = topics.get_topicname(topic_id)
    list = messages.get_messages(topic_id)
    return render_template("admessages.html", user_name=user_name, area_id=area_id, area_name=area_name, topic_id=topic_id, topic_name=topic_name, count=len(list), messages=list)

# Viestin poisto
@app.route("/admin/messagedel/<int:area_id>/<int:topic_id>/<int:message_id>")
def ad_deletem(area_id, topic_id, message_id):
    if messages.admin_delete(message_id):
        return redirect("/admin/messages/"+str(area_id)+"/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin poisto ei onnistunut")

# Admin login
@app.route("/adlogin", methods=["get","post"])
def ad_login():
    if request.method == "GET":
        return render_template("adlogin.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.login(username,password):
            return redirect("/admin/areas")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

#Admin logout
@app.route("/adlogout")
def ad_logout():
    admins.logout()
    return redirect("/admin")

#Uusi admin käyttäjä
@app.route("/adregister", methods=["get","post"])
def ad_register():
    if request.method == "GET":
        return render_template("adregister.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.register(username,password):
            return redirect("/admin/areas")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

# Käyttäjien hallinta
@app.route("/admin/users")
def ad_list_users():
    list = users.get_userlist()
    return render_template("adusers.html", userlist=list)


# Käyttäjän poisto
@app.route("/admin/userdel/<int:user_id>")
def ad_deluser(user_id):
    if users.deleteuser(user_id):
        return redirect("/admin/users")
    else:
        return render_template("error.html",message="Käyttäjän poisto ei onnistunut")
