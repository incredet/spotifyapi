from flask import Blueprint, render_template, request


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", name = "tim")

@views.route("/map", methods = ["POST"])
def songmap():
    artist_name = request.form.get("artist_name")
    return render_template("index.html", name = artist_name)


def create_map():
    pass