from flask import Flask
from flask import render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///varisleo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "avain"
db = SQLAlchemy(app)


@app.route("/")
def index():
    user = None
    if "user_id" in session:
        id = session["user_id"]
        sql = f"SELECT username, id FROM users WHERE id = {id}"
        user = db.session.execute(sql).fetchone()
    return render_template("index.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    sql = f"SELECT password, id FROM users WHERE username = '{username}'"
    result = db.session.execute(sql)
    data = result.fetchone()
    if not data or data[0] != password:
        return redirect("/login")
    session["user_id"] = data[1]
    return redirect("/") 

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form["username"]
    password = request.form["password"]
    sql = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}') RETURNING id"
    user_id = db.session.execute(sql)
    db.session.commit()
    session["user_id"] = user_id.fetchone()[0]
    return redirect("/")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    sql = f"SELECT content FROM messages WHERE content LIKE '%{keyword}%' AND private = FALSE"
    results = db.session.execute(sql).fetchall()
    return render_template("search.html", results=results)

@app.route("/send_message", methods=["POST"])
def send_message():
    content = request.form["message"]
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]
    private = "private" in request.form
    print(private)
    sql = f"INSERT INTO messages (user_id, content, private) VALUES ('{user_id}', '{content}', {private})"
    db.session.execute(sql)
    db.session.commit()
    return redirect("/")

@app.route("/delete_message", methods=["POST"])
def delete_message():
    message_id = int(request.form["msg_id"])
    sql = f"DELETE FROM messages WHERE id = {message_id}"
    db.session.execute(sql)
    db.session.commit()
    return redirect("/user/" + str(session["user_id"]))

@app.route("/user/<int:user_id>")
def user_home(user_id):
    sql = f"SELECT content, id FROM messages WHERE user_id = {user_id}"
    results = db.session.execute(sql).fetchall()
    return render_template("user_page.html", results=results)
