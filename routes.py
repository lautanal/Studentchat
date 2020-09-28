from app import app
from flask import render_template, request, redirect, flash
import users, areas, topics, messages, admins

# Aloitus
@app.route("/")
def index():
    return render_template("index.html")

# Keskustelualueiden listaus
@app.route("/areas")
def list_areas():
    login_id = users.login_id()
    login_alias = users.get_useralias(login_id)
    user_rights = users.get_userrights(login_id)
    list = areas.get_areas(user_rights)
    return render_template("areas.html", login_alias=login_alias, areas=list)

# Viestiketjujen listaus
@app.route("/topics/<int:area_id>")
def list_topics(area_id):
    login_id = users.login_id()
    login_alias = users.get_useralias(login_id)
    area_name = areas.get_areaname(area_id)
    list = topics.get_topics(area_id)
    return render_template("topics.html", login_alias=login_alias, area_id=area_id, area_name=area_name, topics=list)

# Viestien listaus
@app.route("/messages/<int:area_id>/<int:topic_id>")
def list_messages(area_id, topic_id):
    login_id = users.login_id()
    login_alias = users.get_useralias(login_id)
    area_name = areas.get_areaname(area_id)
    topic_name = topics.get_topicname(topic_id)
    list = messages.get_messages(topic_id)
    return render_template("messages.html", login_id=login_id, login_alias=login_alias, area_id=area_id, area_name=area_name, topic_id=topic_id, topic_name=topic_name, count=len(list), messages=list)

# Uusi viesti
@app.route("/new/<int:area_id>/<int:topic_id>")
def new(area_id, topic_id):
    return render_template("new.html", area_id=area_id, topic_id=topic_id, content="")

# Viestin talletus tietokantaan
@app.route("/send/<int:area_id>/<int:topic_id>", methods=["post"])
def send(area_id, topic_id):
    content = request.form["content"]
    if isBlank(content) :
            return render_template("error.html",message="Tyhjä kenttä, viestiä ei talletettu")
    if messages.insert(topic_id, content, None):
        return redirect("/messages/"+str(area_id)+"/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin talletus ei onnistunut")

# Viestin muuttaminen
@app.route("/modify/<int:area_id>/<int:topic_id>/<int:message_id>")
def modify(area_id, topic_id, message_id):
    content = messages.read_message(message_id)
    return render_template("modify.html", area_id=area_id, topic_id=topic_id, message_id=message_id, content=content)

# Muutetun viestin talletus tietokantaan
@app.route("/update/<int:area_id>/<int:topic_id>/<int:message_id>", methods=["post"])
def update(area_id, topic_id, message_id):
    content = request.form["content"]
    if isBlank(content) :
            return render_template("error.html",message="Tyhjä kenttä, viestin talletus ei onnistunut")
    if messages.update(message_id, content):
        return redirect("/messages/"+str(area_id)+"/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin talletus ei onnistunut")

# Viestin poisto (näkyviltä)
@app.route("/messagedel/<int:area_id>/<int:topic_id>/<int:message_id>")
def deletem(area_id, topic_id, message_id):
    if messages.delete(message_id):
        return redirect("/messages/"+str(area_id)+"/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin poisto ei onnistunut")

#Viestiin vastaaminen
@app.route("/reply/<int:area_id>/<int:topic_id>/<int:message_id>")
def reply(area_id, topic_id, message_id):
    user_id = messages.get_author(message_id)
    author = users.get_useralias(user_id)
    message = messages.read_message(message_id)
    return render_template("reply.html", area_id=area_id, topic_id=topic_id, content="", reply_id=message_id, author=author, message=message)

# Vastauksen talletus tietokantaan
@app.route("/sendreply/<int:area_id>/<int:topic_id>/<int:reply_id>", methods=["post"])
def send_reply(area_id, topic_id, reply_id):
    content = request.form["content"]
    if isBlank(content) :
            return render_template("error.html",message="Tyhjä kenttä, viestiä ei talletettu")
    if messages.insert(topic_id, content, reply_id):
        return redirect("/messages/"+str(area_id)+"/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin talletus ei onnistunut")

# Uusi viestiketju
@app.route("/newtopic/<int:area_id>")
def newtopic(area_id):
    return render_template("newtopic.html", area_id=area_id)

# Uuden viestiketjun talletus tietokantaan
@app.route("/topicsend/<int:area_id>", methods=["post"])
def topicsend(area_id):
    topic_name = request.form["topicname"]
    if isBlank(topic_name) :
            return render_template("error.html",message="Tyhjä kenttä, viestiketjua ei aloitettu")
    if topics.sendtopic(area_id, topic_name):
        return redirect("/topics/"+str(area_id))
    else:
        return render_template("error.html",message="Viestiketjun talletus ei onnistunut")

# Login
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
#            flash("Väärä tunnus tai salasana")
            return render_template("login.html")

# Logout
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

# Uusi käyttäjä
@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        alias = request.form["alias"]
        if isBlank(username) or isBlank(password) or isBlank(alias) :
             return render_template("error.html",message="Tyhjä kenttä, rekisteröintiä ei tehty")
        if users.register(username,password,alias):
            return redirect("/areas")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

def isBlank (myString):
    return not (myString and myString.strip())

