from flask import Flask , render_template , Blueprint
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login')
def login() :
    return 'login'

@auth.route('/signup')
def signup() :
    return 'signup'

    