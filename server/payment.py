from flask import Flask , render_template , Blueprint
from . import db

pay = Blueprint('pay',__name__)

@pay.route('/pay')
def payment() :
    return 'pay'