from flask import Flask
from  flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def create_app() :
     app = Flask(__name__, static_url_path="", template_folder = "../client/templates", static_folder="../client")

     app.config['SECRET_KEY'] = 'blackcat'
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yujjcgbcxipdsn:4f88cb27f0f30b83ba9246da1d235785227cd8540872973f2425067465dfdf2f@ec2-52-22-216-69.compute-1.amazonaws.com:5432/d7cq6od5bn0ea5'

     db.init_app(app)

     # blueprint for auth routes in our app
     from .auth import auth as auth_blueprint
     app.register_blueprint(auth_blueprint)

     # blueprint for non-auth parts of app
     from .main import main as main_blueprint
     app.register_blueprint(main_blueprint)

     # blueprint from payment parts of app
     from .payment import pay as payment_blueprint
     app.register_blueprint(payment_blueprint)

     # blueprint for booking ticket parts of app 
     from .bookticket import book as booking_blueprint
     app.register_blueprint(booking_blueprint)

     return app

