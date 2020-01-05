from hashlib import md5
import urllib, hashlib
from datetime import datetime
from flask import Flask, escape, request, render_template, redirect ,session ,flash
import sqlite3
from passlib.hash import sha256_crypt
from functools import wraps
from flask_avatars import Avatars


def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'user_id' in session:
			return f(*args, **kwargs)
		else:
			return redirect('/login')
	return wrap

app = Flask(__name__)
avatars = Avatars(app)
app.secret_key = 'LOL'

@app.route('/')
@login_required
def hello():
	conn = sqlite3.connect('users')
	c = conn.cursor()
	info = c.execute("SELECT * FROM info WHERE user=:user",{"user":session["user_id"]}).fetchone()
	conn.commit()
	user = session["user_id"]
	status = c.execute(f"SELECT * FROM {user}")
	return render_template("index.html",info = info,status=status)
	conn.commit()
	conn.close()

@app.route('/register',methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		conn = sqlite3.connect('users')
		c = conn.cursor()
		u_name = request.form.get("username")
		name = request.form.get("name")
		password = (request.form.get("password"))
		email = request.form.get("email")
		dob = request.form.get("age")
		age = datetime.now().year - int(dob[0:4])
		if not name or not password or not email or not u_name or not dob:
			flash("ONE OR MORE FEILD ARE NOT LEFT EMPTY DURING SUBMISSION")
			return redirect('/register')
		elif password != request.form.get("confirmation"):
			flash("PASSWORDS DON'T MATCH")
			return redirect('/register')
		if c.execute("SELECT * FROM info WHERE user =:user",{"user":name}).fetchone() != None:
			flash("USERNAME ALREADY EXISTS")
			return redirect("/register")
		if c.execute("SELECT * FROM info WHERE email =:email",{"email":email}).fetchone() != None:
			flash("EMAIL ALREADY EXISTS")
			return redirect("/register")
		passw = sha256_crypt.hash(password)
		avatar_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
		c.execute("INSERT INTO info(user,pass,email,avatar,dob,age,name) VALUES(?,?,?,?,?,?,?)", (u_name, passw,email,avatar_hash,dob,age,name))
		c.execute(f"CREATE TABLE {u_name} ('s_no' INTEGER PRIMARY KEY NOT NULL, 'post' TEXT NOT NULL, 'ddmmyy' DATETIME NOT NULL)")
		conn.commit()
		conn.close()
		return redirect("/")
	elif request.method == 'GET':
		return render_template("register.html")

@app.route('/home')
def home():
	return redirect("/")


@app.route('/login',methods=['POST','GET'])
def login():
	if request.method == 'POST':
		session.clear()
		name = request.form.get("username")
		password = request.form.get("password")
		if not name or not password:
			flash("ONE OR MORE FIELDS ARE LEFT EMPTY")
			return redirect('/login')
		conn = sqlite3.connect('users')
		c = conn.cursor()
		row = c.execute("SELECT * FROM info WHERE user = :name", {"name":name})
		data = c.fetchone()
		if data == None:
			flash("BRU.. u have to register to login, that's how these things work i guess")
			return redirect('/login')
		passw = data[1]
		if sha256_crypt.verify(password,passw):
			session["user_id"] = data[0]
		else:
			flash("INCORRECT PASSWORD")
			return redirect("/login")
		conn.commit()
		conn.close()
		return redirect("/")
	else:
		return render_template("login.html")

@app.route('/logout',methods=['POST','GET'])
def logout():
	session.clear()
	return redirect('/')


@app.route('/feed' ,methods=['GET','POST'])
@login_required
def feed():
	if request.method == 'POST':
		status = request.form.get("status")
		user = session["user_id"]
		conn = sqlite3.connect('users')
		c = conn.cursor()
		avatar = c.execute("SELECT avatar FROM info WHERE user=:user",{"user":user}).fetchone()[0]
		c.execute(f"INSERT INTO {user}(post,ddmmyy) VALUES(?,?)",(status,datetime.now()))
		c.execute("INSERT INTO status(user,post,ddmmyy,avatar) VALUES(?,?,?,?)",(user,status,datetime.now(),avatar))
		conn.commit()
		data = c.execute("SELECT * FROM status")
		return render_template("feed.html",data = data)
		conn.commit()
		conn.close()
	else:
		conn = sqlite3.connect('users')
		c = conn.cursor()
		data = c.execute("SELECT * FROM status")
		return render_template("feed.html",data = data)
		conn.commit()
		conn.close()

@app.route('/people' ,methods=['GET','POST'])
@login_required
def people():
	if request.method == 'POST':
		search = request.form.get("search")
		conn = sqlite3.connect('users')
		c = conn.cursor()
		data = c.execute("SELECT * FROM info WHERE user= :user",{"user":search})
		return render_template("find_people.html",data=data)
		conn.commit()
		conn.close()
	else:
		conn = sqlite3.connect('users')
		c = conn.cursor()
		data = c.execute("SELECT * FROM info")
		return render_template("find_people.html",data=data)
		conn.commit()
		conn.close()

@app.route('/user' ,methods=['GET','POST'])
@login_required
def user():
	if request.method == 'POST':
		user = request.form.get("button")
		if user == session["user_id"]:
			return redirect('/')
		conn = sqlite3.connect('users')
		c = conn.cursor()
		info = c.execute("SELECT * FROM info WHERE user=:user",{"user":user}).fetchone()
		conn.commit()
		status = c.execute(f"SELECT * FROM {user}")
		return render_template("user.html",info = info,status=status)
		conn.commit()
		conn.close()

@app.route('/status',methods=['POST','GET'])
@login_required
def redirect_status():
	return render_template('status.html')

@app.route('/edit',methods=['POST','GET'])
@login_required
def edit():
	status = request.form.get("edit")
	conn = sqlite3.connect('users')
	c = conn.cursor()
	c.execute("UPDATE info SET status = :status WHERE user =:user",{"status":status,"user":session["user_id"]})
	conn.commit()
	conn.close()
	return redirect('/')

#if __name__ == "__main__":
#    app.run(debug=True)
