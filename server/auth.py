from flask import Flask , render_template , Blueprint , request , make_response , redirect , url_for , flash
from uuid import uuid4
import json
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login')
def render_login() :
    msg = request.args.get('msg')
    return render_template('login.html' , msg = msg  ,username = None)


@auth.route('/login',methods=['POST'])
def login_user() :
    email  = request.form.get('email')
    password = request.form.get('password')
    result  = db.session.execute('select password,  uid , name  from users where email = :email',{'email':email}).fetchall()

    if len(result) == 0 :
        msg = "user doesnt exist "
        print(msg)
        resp = make_response(render_template("login.html", msg = msg , username = None))

    else :
        
        (pas,uid,name) = result[0]
        if password == pas :
            msg = 'Successful login'
            print(msg)
            
            data = {
                'uid':str(uid),
                'name':name
            }

            print(data,json.dumps(data))
            resp = make_response(redirect(url_for('main.render_home', msg = msg )))
            resp.set_cookie('data',json.dumps(data))
            
        else :
            msg = 'Username or Password does not match'
            print(msg)
            resp = make_response(render_template("login.html", msg = msg , username = None))

    return resp



@auth.route('/logout',methods=['GET'])
def logoutUser() :
    uid = request.cookies.get('data')
    print(uid)
    resp = make_response(redirect(url_for('main.render_home' , msg = "User Logged Out Successfully")))
    resp.set_cookie('data','',expires = 0)

    return resp


@auth.route('/signup',methods=['GET'])
def render_signup() :
    msg = request.args.get('msg')
    return render_template('signup.html',msg = msg , username = None)


@auth.route('/signup',methods=['POST'])
def signup_user() :
    username  = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    phno = request.form.get('phno')

    result  = db.session.execute('select uid from users where email = :email',{'email' : email}).fetchall()

    if len(result) == 0 :
        db.session.execute("insert into users (uid , name , email , ph_no , password) values (:uid,:username,:email,:ph_no,:password)",{'uid':uuid4().int%123456789 , 'username':username , 'email':email , 'ph_no':phno , 'password':password})
        db.session.commit()
        return redirect(url_for('auth.render_login',msg = 'Sign Up Successful , Login To continue'))
    else :
        print('already exist')
        return redirect(url_for('auth.render_login',msg = 'Login To Continue'))


    


    