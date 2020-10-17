from flask import Flask, render_template,request,redirect,url_for
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
app = Flask(__name__)

def createtable():
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    table="""
        CREATE TABLE students (
            name TEXT,
            activity TEXT
        )
        """
    cur.execute(table)
    con.commit()

def enter_data(n,a):
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    sqlite_insert_with_param = f"INSERT INTO students(name,activity) VALUES ('{n}','{a}');"
    cur.execute(sqlite_insert_with_param)
    con.commit()
    con.close()

def update(n,a):
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    sqlite_insert_with_param = f"UPDATE students SET activity = '{a}' WHERE name = '{n}';"
    cur.execute(sqlite_insert_with_param)
    con.commit()
    con.close()

def delete(name):
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur=con.cursor()
    sqlite_insert_with_param = f"DELETE FROM students WHERE name = '{name}';"
    cur.execute(sqlite_insert_with_param)
    con.commit()

def retrieve():
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    users = cur.fetchall()
    con.close()
    return users

@app.route("/")
def main():
    try:createtable()
    except:pass
    return redirect(url_for("home"))

@app.route("/home",methods=["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        enter = True
        n = request.form['name']
        a = request.form['activity']
        data = retrieve()
        for i in data:
            if i[0] == n:
                update(n,a)
                enter = False
        if enter:
            enter_data(n,a)
        return redirect(url_for("registered", name = n, activity = a))

@app.route("/registered/<name>/<activity>")
def registered(name,activity):
    return render_template("registered.html", name = name, activity = activity)

@app.route("/ban/<password>",methods=["GET","POST"])
def ban(password):
    if password == os.environ['PASSWORD']:
        if request.method == "GET":
            return render_template("ban.html")
        else:
            ban = request.form['name']
            delete(ban)
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/registered/<password>/data")
def data(password):
    if password == os.environ['PASSWORD']:
        d=retrieve()
        return render_template("data.html", info = d)
    else:
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
