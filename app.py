from flask import Flask, render_template, request, session, redirect
import sys
import sqlite3
from sqlite3 import Error

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
# Registers a new user
def register():
    # Configures SQLite database
    db=sqlite3.connect('chess')
    cursor=db.cursor()
    
    # # Forgets any existing userID
    # session.clear()
    
    # User reached route via POST
    if request.method=="POST":

        # Ensure username was submitted

        # Ensure password was submitted

        # ensure that the two passwords match

        username=request.form.get("username")
        password=request.form.get("password")

        script="INSERT INTO users (user_name, password) VALUES (%s, %s)"
        values=(username, password)
        # Insert user info into database
        cursor.execute(script, values)
        # Redirect the user back to the homepage
        return redirect('/')
    # User reached route via GET
    else:
        return render_template("register.html")



if __name__=="__main__":
    app.run()

