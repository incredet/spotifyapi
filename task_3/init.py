""" initialize file
"""
from flask import Flask
from blueprint import views

app = Flask(__name__)

app.config["SECRET_KEY"] = 'incredet'
app.register_blueprint(views, url_prefix = "/")


if __name__ == "__main__":
    app.run(debug = True, port = 8000)
