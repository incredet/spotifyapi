""" blueprint """
from search import create_map
from flask import Blueprint, render_template, request


views = Blueprint(__name__, "views")

@views.route("/")
def home():
    """ homepage func
    """
    return render_template("index.html")

@views.route("/map", methods = ["POST"])
def songmap():
    """ gets map and gets request
    """
    artist_name = request.form.get("artist_name")
    create_map(artist_name)
    return render_template("available_markets.html")
