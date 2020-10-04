from app import app
from flask import render_template, request, redirect, flash, Markup
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
@app.route("/messages/<int:topic_id>")
def list_messages(topic_id):
    login_id = users.login_id()
    login_alias = users.get_useralias(login_id)
    topic_name = topics.get_topicname(topic_id)
    area_id = topics.get_area_id(topic_id)
    area_name = areas.get_areaname(area_id)
    list = messages.get_messages(topic_id)
#    print("VIESTILISTA:")
#    print(len(list))
    return render_template("messages.html", login_id=login_id, login_alias=login_alias, area_id=area_id, area_name=area_name, topic_id=topic_id, topic_name=topic_name, count=len(list), messages=list)
    
# viestien haku
@app.route("/find")
def find():
    return render_template("find.html")

# Viestin haku inputin perusteella
@app.route("/findmsg", methods=["post"])
def findmsg():
    login_id = users.login_id()
    login_alias = users.get_useralias(login_id)
    user_search = request.form["user_search"].strip()
    text_search = request.form["text_search"].strip()
    if isBlank(user_search) and isBlank(text_search) :
        return render_template("find.html",error="Tyhjät kentät, hakua ei tehty")
    list = messages.find_messages(user_search, text_search)
#    if user_search == "":
#       user_search = "%20"
#    if text_search == "":
#        text_search = "%20"
    return render_template("findmsg.html", login_id=login_id, login_alias=login_alias, count=len(list), messages=list, user_search=user_search, text_search=text_search)

# Uusi viesti
@app.route("/new/<int:topic_id>")
def new(topic_id):
    return render_template("new.html", topic_id=topic_id, content="")

# Viestin talletus tietokantaan
@app.route("/send/<int:topic_id>", methods=["post"])
def send(topic_id):
    content = request.form["content"]
    if isBlank(content) :
            return render_template("new.html", topic_id=topic_id, content="", error="Tyhjä kenttä, viestiä ei talletettu")
    if messages.insert(topic_id, content, None):
        return redirect("/messages/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin talletus ei onnistunut")

# Viestin muuttaminen
@app.route("/modify/<int:message_id>")
def modify(message_id):
    content = messages.read_message(message_id)
    return render_template("modify.html", message_id=message_id, content=content)

# Muutetun viestin talletus tietokantaan
@app.route("/update/<int:message_id>", methods=["post"])
def update(message_id):
    topic_id = messages.get_topic_id(message_id)
    content = request.form["content"]
    if isBlank(content) :
            return render_template("error.html",message="Tyhjä kenttä, viestin talletus ei onnistunut")
    if messages.update(message_id, content):
        return redirect("/messages/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin talletus ei onnistunut")

# Viestin muuttaminen, paluu etsintäsivulle
@app.route("/modify2/<int:message_id>/<string:user_search>/<string:text_search>")
def modify2(message_id, user_search, text_search):
    content = messages.read_message(message_id)
    if text_search == "":
        text_search = "%20"
    return render_template("modify2.html", message_id=message_id, content=content, user_search=user_search, text_search=text_search)

# Muutetun viestin talletus tietokantaan, paluu etsintäsivulle
@app.route("/update2/<int:message_id>/<string:user_search>/<string:text_search>", methods=["post"])
def update2(message_id, user_search, text_search):
    content = request.form["content"]
    if isBlank(content) :
            return render_template("error.html",message="Tyhjä kenttä, viestin talletus ei onnistunut")
    if messages.update(message_id, content):
        login_id = users.login_id()
        login_alias = users.get_useralias(login_id)
        list = messages.find_messages(user_search.strip(), text_search.strip())
        return render_template("findmsg.html", login_id=login_id, login_alias=login_alias, count=len(list), messages=list, user_search=user_search, text_search=text_search)
    else:
        return render_template("error.html",message="Viestin talletus ei onnistunut")

# Viestin poisto (näkyviltä)
@app.route("/messagedel/<int:message_id>")
def deletem(message_id):
    topic_id = messages.get_topic_id(message_id)
    if messages.delete(message_id):
        return redirect("/messages/"+str(topic_id))
    else:
        return render_template("error.html",message="Viestin poisto ei onnistunut")

# Viestin poisto, paluu etsintäsivulle
@app.route("/messagedel2/<int:message_id>/<string:user_search>/<string:text_search>")
def deletem2(message_id, user_search, text_search):
    topic_id = messages.get_topic_id(message_id)
    if messages.delete(message_id):
        login_id = users.login_id()
        login_alias = users.get_useralias(login_id)
        list = messages.find_messages(user_search.strip(), text_search.strip())
        return render_template("findmsg.html", login_id=login_id, login_alias=login_alias, count=len(list), messages=list, user_search=user_search, text_search=text_search)
    else:
        return render_template("error.html",message="Viestin poisto ei onnistunut")

# Viestiin vastaaminen
@app.route("/reply/<int:message_id>")
def reply(message_id):
    user_id = messages.get_user_id(message_id)
    author = users.get_useralias(user_id)
    message = messages.read_message(message_id)
    topic_id = messages.get_topic_id(message_id)
    return render_template("reply.html", content="", message_id=message_id, author=author, message=message)

# Vastauksen talletus tietokantaan
@app.route("/sendreply/<int:message_id>", methods=["post"])
def send_reply(message_id):
    user_id = messages.get_user_id(message_id)
    topic_id = messages.get_topic_id(message_id)
    author = users.get_useralias(user_id)
    message = messages.read_message(message_id)
    ref_msg = author + " kirjoitti: \n" + message
    content = request.form["content"]
    if isBlank(content) :
#            return render_template("error.html",message="Tyhjä kenttä, viestiä ei talletettu")
        return render_template("reply.html", content="", message_id=message_id, author=author, message=message,error="Tyhjä kenttä, viestiä ei talletettu")
    if messages.insert(topic_id, content, ref_msg):
        return redirect("/messages/"+str(topic_id))
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
            return render_template("newtopic.html", area_id=area_id, error="Tyhjä kenttä, viestiketjua ei aloitettu")
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

