from flask import Blueprint, render_template, request
from search import create_map


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", name = "tim")

@views.route("/map", methods = ["POST"])
def songmap():
    artist_name = request.form.get("artist_name")
    create_map(artist_name)
    return render_template("available_markets.html")
