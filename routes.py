from app import app
from flask import render_template, request, redirect
import users, areas, topics, messages

#Aloitus
@app.route("/")
def index():
    return render_template("index.html")

#Viestialueiden listaus
@app.route("/areas")
def list_areas():
    user_name = users.get_useralias()
    user_rights = users.get_userrights()
    list = areas.get_areas(user_rights)
    return render_template("areas.html", user_name=user_name, areas=list)

#Viestiketjujen listaus
@app.route("/topics/<int:area_id>")
def list_topics(area_id):
#    print("ID = " + str(area_id))
    user_name = users.get_useralias()
    area_name = areas.get_areaname(area_id)
    list = topics.get_topics(area_id)
    return render_template("topics.html", user_name=user_name, area_id=area_id, area_name=area_name, topics=list)

#Viestien listaus
@app.route("/messages/<int:area_id>/<int:topic_id>")
def list_messages(area_id, topic_id):
    user_id = users.user_id()
    user_name = users.get_useralias()
    area_name = areas.get_areaname(area_id)
    list = messages.get_messages(topic_id)
    topic_name = topics.get_topicname(topic_id)
    return render_template("messages.html", user_id=user_id, user_name=user_name, area_id=area_id, area_name=area_name, topic_id=topic_id, topic_name=topic_name, count=len(list), messages=list)

#Uusi viesti
@app.route("/new/<int:area_id>/<int:topic_id>")
def new(area_id, topic_id):
    return render_template("new.html", area_id=area_id, topic_id=topic_id)

#Viestin talletus tietokantaan
@app.route("/send/<int:area_id>/<int:topic_id>", methods=["post"])
def send(area_id, topic_id):
    content = request.form["content"]
    if messages.send(topic_id, content):
        return redirect("/messages/"+str(area_id)+"/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin lähetys ei onnistunut")

#Viestin muuttaminen
@app.route("/modify/<int:area_id>/<int:topic_id>/<int:message_id>")
def modify(area_id, topic_id, message_id):
    content = messages.read_message(message_id)
    return render_template("modify.html", area_id=area_id, topic_id=topic_id, message_id=message_id, content=content)

#Muutetun viestin talletus tietokantaan
@app.route("/modsave/<int:area_id>/<int:topic_id>/<int:message_id>", methods=["post"])
def modsave(area_id, topic_id, message_id):
    content = request.form["content"]
    if messages.modify(message_id, content):
        return redirect("/messages/"+str(area_id)+"/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin lähetys ei onnistunut")

#Viestin poisto
@app.route("/messagedel/<int:area_id>/<int:topic_id>/<int:message_id>")
def deletem(area_id, topic_id, message_id):
    if messages.delete(message_id):
        return redirect("/messages/"+str(area_id)+"/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin lähetys ei onnistunut")

#Uusi viestiketju
@app.route("/newtopic/<int:area_id>")
def newtopic(area_id):
    return render_template("newtopic.html", area_id=area_id)

#Uuden viestiketjun talletus tietokantaan
@app.route("/topicsend/<int:area_id>", methods=["post"])
def topicsend(area_id):
    topic_name = request.form["topicname"]
    if topics.sendtopic(area_id, topic_name):
        return redirect("/topics/"+str(area_id))
    else:
        return render_template("error.html",message="Viestiketjun talletus ei onnistunut")

#Login
@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/areas")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

#Logout
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

#Uusi käyttäjä
@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        alias = request.form["alias"]
        if users.register(username,password,alias):
            return redirect("/areas")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")