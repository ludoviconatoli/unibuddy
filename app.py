from flask import Flask
from flask import render_template
from project import app

@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)