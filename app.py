from flask import Flask, render_template
import sys

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
# Registers a new user
def register():
    pass

if __name__=="__main__":
    app.run()

