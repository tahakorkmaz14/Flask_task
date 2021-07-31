from flask import Blueprint

site = Blueprint('site', __name__)

# basic regular welcome page


@site.route('/')
def index():
    return '<h1>Welcome to the home page for distance calculator to MKAD Line !</h1>'
