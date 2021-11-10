from flask import Flask, render_template, request, session, redirect
import sys
from app_helper import login_required
from flask_session import Session
import sqlite3
from tempfile import mkdtemp
from sqlite3 import Error
import pandas as pd

from app_helper import login_required

app=Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
# Registers a new user
def register():
    # Configures SQLite database
    db=sqlite3.connect("chess")
    c=db.cursor()
    
    # Forgets any existing userID
    session.clear()
    
    # User reached route via POST
    if request.method=="POST":

        # Ensure username was submitted

        # Ensure password was submitted

        # ensure that the two passwords match

        username=request.form.get("username")
        password=request.form.get("password")

        script="INSERT INTO users (user_name, password) VALUES (?, ?)"
        values=(username, password)
        # Insert user info into database
        c.execute(script, values)
        db.commit()

        # Redirect the user back to the homepage
        return redirect('/')
    # User reached route via GET
    else:
        return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
# Logs the user in
def login():

    # Configures SQLite database
    db=sqlite3.connect("chess")
    c=db.cursor()
    
    # Forget any current user_id
    session.clear()

    # User reached route via POST
    if request.method=="POST":

        # Ensure username was submitted
        
        # Ensure password was submitted

        # Query database for username
        script="SELECT * FROM users WHERE user_name=?"
        username=request.form.get("username")
        c.execute(script, username)

        # Loads SQLite object into a dataframe
        df=pd.DataFrame(c.fetchall(), columns=['user_id', 'user_name', 'password'])

        # Ensure username exists and password is correct 

        # Remember which user has logged in
        user_data=df.loc[df['user_name']=='k'].values[0]
        session["user_id"]=user_data[0]

        # Redirect user to home page
        return redirect("/")
    
    # User reached route via GET
    else:
        return render_template("login.html")

@app.route("/logout")
# Logs the user out
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/lobby")
@login_required
# Renders the online lobby
def lobby():
    return render_template("lobby.html")

if __name__=="__main__":
    app.run()

