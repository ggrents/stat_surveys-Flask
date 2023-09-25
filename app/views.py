from flask import render_template, url_for

from app import main_app


@main_app.route("/")
def index():
    return render_template("index.html", list=[1, 2, 3])


@main_app.route("/main")
def main():
    return render_template("main.html")
