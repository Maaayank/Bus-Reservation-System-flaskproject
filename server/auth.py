from flask import Flask , render_template , Blueprint , request
from smalluuid import SmallUUID as uuid 
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login')
def render_login() :
    return 'login'


@auth.route('/login',methods=['POST'])
def login_user() :
    username  = request.form.get('username')
    password = request.form.get('password')

    result  = db.session.execute('select uid from users where email = :username',{'username':email})

    if len(result) == 0 :
        print("user doesnt exist ")
    else :
        result2 = db.session.execute('select password from users where email = :username',{'username':email})
        if password == result2.first()[0] :
            print('user logged in')
        else :
            print('user logged in ')


@auth.route('/signup')
def render_signup() :
    return 'signup'

@auth.route('/signup',methods=['POST'])
def signup_user() :
    username  = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    phno = request.form.get('phno')

    result  = db.session.execute('select uid from users where uis = :uid')

    if len(result) == 0 :
        db.session.execute("insert into users (uid , name , email , ph_no , password) values (:uid,:username,:email,:ph_no,:password)",{'uid':uuid.int%123456789 , 'name':username , 'email':email , 'ph_no':phno , 'password':password})
    else :
        print('already exist')

    


    