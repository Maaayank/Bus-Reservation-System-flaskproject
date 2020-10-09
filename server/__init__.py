from flask import Flask
from  flask_sqlalchemy import SQLAlchemy 

print('hii')
db = SQLAlchemy()

def create_app() :
     
     app = Flask(__name__,template_folder = "../client/templates",static_folder='../client/')

     app.config['SECRET_KEY'] = 'blackcat'
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/BTRS'

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

