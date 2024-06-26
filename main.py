from flask import Flask, render_template, request, session, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/GreenHive"
mongo = PyMongo(app)
db = mongo.db
app.secret_key = 'SECRET_KEY'
logged_in = False

@app.route("/", methods = ['GET', 'POST'])
def Home():
    logged_in = session.get('logged_in', False)
    if logged_in:
        status = "Sign Out"
    else:
        status = "Login"
    if request.method == 'POST':
        if logged_in:
            print("Logged in")
            session.pop('logged_in', None)
            return redirect('/login')
        else:
            print("Logged out")
            status = "Login"
            return redirect('/login')
    return render_template("home.html", login=status)

@app.route("/login", methods = ['GET','POST'])
def login():
    # database = {"pv":"123","rs":"456","rt":"789"}
    info = ""
    if request.method == "POST":
        username = request.form["username"]
        pwd = request.form["pwd"]
        username_check = db.accounts.find_one({'username': username})
        if not username_check:
            info = "Username does not exist"
        elif username_check and username_check['password'] != pwd:
            info = "Wrong password!"
        elif username_check and username_check['password'] == pwd:
            logged_in = True
            session['logged_in'] = logged_in
            logged_in = True
            return render_template("home.html", login="Sign Out")
        return render_template("index.html", info=info)
    return render_template("index.html", info=info)

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("you re on register")
    error = ""
    if request.method == 'POST':
        error = ""
        username = request.form["username"]
        pwd = request.form["pwd"]
        confirm_password = request.form["confirm-pwd"]
        location = request.form["location"]
        con_no = request.form["contact-num"]
        if len(username) < 4:
            error = 'Username too short.'
        if pwd != confirm_password:
            print("what")
            error = 'Passwords do not match.'
        if error == "":
            db.accounts.insert_one({"username": username, "password": pwd, "location": location, "contact-number": con_no})
            return render_template('index.html', info="Registeration successful!")
    return render_template('register.html', error=error)


@app.route('/feed',methods=['GET','PUT'])
def feed():
    logged_in = session.get('logged_in', False)
    error = None
    if not logged_in:
        return render_template('loggedout.html')
    return render_template('feed.html', error=error)

@app.route('/search',methods=['GET','POST'])
def search():
    logged_in = session.get('logged_in', False)
    error = None
    if not logged_in:
        return render_template('loggedout.html')
    return render_template('search.html', error=error)

if __name__ == "__main__":
    app.run(debug= True)
