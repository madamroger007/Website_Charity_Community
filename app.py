from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv
from os.path import join, dirname
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect, generate_csrf,validate_csrf
from validation.forms import RegistrationForm,LoginForm ,DonateForm
from werkzeug.utils import secure_filename


#************************* Variable & Key *****************************
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


#* config flask
app = Flask(__name__, template_folder='templates')
csrf = CSRFProtect(app)

app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    MONGODB_URI=os.environ.get("MONGODB_URI"),
    DB_NAME=os.environ.get("DB_NAME"),
    TOKEN_KEY=os.environ.get("TOKEN_KEY"),
    TEMPLATE_AUTO_RELOAD=True,
    UPLOAD_FOLDER=["./static/assets/img/news", "./static/assets/img/projects", "./static/assets/img/users"],
)

#* Connect database
client = MongoClient(app.config["MONGODB_URI"])
db = client[app.config["DB_NAME"]]


# * Function Helper
def decode_token(payload):
    token = jwt.decode(payload, app.config["SECRET_KEY"], algorithms=["HS256"])
    return token


def encode_token(payload):
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token


#************************* Login & Register client || admin *****************************

@app.route("/register/<role>", methods=["POST", 'GET'])
def register(role):
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username_give.data
        fullname = form.fullname_give.data
        email = form.email_give.data
        password = form.password_give.data
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        exists = bool(db.users.find_one({"username": username}))
        if exists :
             return jsonify({"result": "success", "exists": exists})
        default_role = role if role == 'admin' else 'users'
        doc = {
        "username": username,
        "full_name": fullname,
        "password": password_hash,
        "role": default_role,
        "profile_info": "unknown",
        "profile_img": "static/assets/img/users/profile/users.png",
        "email": email,
        "country":"unknown" ,
        "no_hp":"unknown" ,
        "address":"unknown" ,
        "maps":"unknown" ,
        "profile_img_bg": "static/assets/img/users/bg/bg_users.jpg",

        }

        db.users.insert_one(doc)
        return redirect(url_for('login'))
   
    return render_template("auth/register.html",form=form,role=role)

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        # Regular login process
        username = form.username_give.data
        password = form.password_give.data
        pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        user = db.users.find_one(
            {
                "username": username,
                "password" : pw_hash,
            })

        if user:
            payload = {
                "username": username,
                "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
            }
            token = encode_token(payload)
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    "result": "success",
                    "token": token,
                })
            else:
                msg = "Invalid username or password"
                return render_template("auth/login.html", token=token, form=form, msg=msg)

        else:
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({ "result": "fail","msg": "We could not find a user with that id/password combination" })         
            else:
                msg = "Invalid username or password"  # Assuming you are using Flask's flash messages
                return redirect(url_for("login", msg=msg))
    else:
        return render_template("auth/login.html", form=form)

#**************************************** Client ****************************************
@app.route('/')
def index():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})        
        if user_info["role"] == 'admin':
            return redirect(url_for('dashboard'))  
        else:
            return render_template('client/index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        msg = "Your token has expired"
        return redirect(url_for("login", msg=msg))
    except jwt.exceptions.DecodeError:
        msg = "There was a problem logging your in"
        return redirect(url_for("login", msg=msg))
 
@app.route('/about')
def about():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(user_info)
        return render_template('client/about.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

@app.route('/news')
def news():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(user_info)
        return render_template('client/news.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

@app.route('/donate')
def donate():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        return render_template('client/donate.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

@app.route('/donate/payment',  methods=['POST', 'GET'])
def donate_pay():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    form = DonateForm()
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(form.agree_give.data)

        if request.method == 'POST' and form.validate_on_submit():
        # Handle the form submission, store data in MongoDB
            print("hallo ini saya")
            print(form.email_give.data)
            donation_data = {
            "username":user_info.get("username"),
            "country": form.country_give.data,
            "donation_amount": form.donate_give.data,
            "email": form.email_give.data,
            "agree": form.agree_give.data,
            "phone": form.phone_give.data,
            "bank_account": form.rekening_give.data,
            "expiry_date": form.expiry_date_give.data,
            "security_code": form.security_code_give.data,
            "full_name": form.fullname_give.data,
            }

        # Insert the data into the MongoDB collection (adjust collection name as needed)
            # db.donations.insert_one(donation_data)
            return redirect(url_for('donate'))
      
        return render_template('client/payment.html', user_info=user_info,form=form)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

@app.route('/project')
def project():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        return render_template('client/project.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


@app.route('/contact_us')
def contact_us():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(user_info)
        return render_template('client/contact.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    

@app.route('/profile')
def profile():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(user_info)
        return render_template('client/profile.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
#*************************************** Admin *****************************************
@app.route('/dashboard/admin')
def dashboard():
    return render_template('admin/index.html')

@app.route('/dashboard/admin/users')
def users_admin():
    return render_template('admin/table-users.html')

@app.route('/dashboard/admin/news')
def news_admin():
    return render_template('admin/table-news.html')

@app.route('/dashboard/admin/project')
def project_admin():
    return render_template('admin/table-project.html')

@app.route('/dashboard/admin/donate')
def donate_admin():
    return render_template('admin/table-donate.html')

@app.route('/dashboard/admin/profile')
def profile_admin():
    return render_template('admin/pages-profile.html')



if __name__ == '__main__':
    app.run(debug=True)
 