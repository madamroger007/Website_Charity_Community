from flask import Blueprint,render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv
from os.path import join, dirname
import os
from validation.forms import RegistrationForm, LoginForm



auth_bp = Blueprint('auth', __name__)

dotenv_path = join(dirname(dirname(__file__)), ".env")
load_dotenv(dotenv_path)

SECRET_KEY=os.environ.get("SECRET_KEY")
MONGODB_URI=os.environ.get("MONGODB_URI")
DB_NAME=os.environ.get("DB_NAME")
TOKEN_KEY=os.environ.get("TOKEN_KEY")

# * Connect database
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]


# * Function Helper
def decode_token(payload):
    token = jwt.decode(payload, SECRET_KEY, algorithms=["HS256"])
    return token


def encode_token(payload):
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# ************************* Login & Register client || admin *****************************

@auth_bp.route("/register/<role>", methods=["POST", 'GET'])
def register(role):
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        # time
        time_now = datetime.now()
        time_str = time_now.strftime("%Y-%m-%d-%H-%M-%S")
        username = form.username_give.data
        fullname = form.fullname_give.data
        email = form.email_give.data
        password = form.password_give.data
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        exists = bool(db.users.find_one({"username": username}))
        if exists:
            return jsonify({"result": "success", "exists": exists,"msg":"User ada"})
        default_role = role if role == 'admin' else 'users'
        doc = {
            "username": username,
            "fullname": fullname,
            "password": password_hash,
            "role": default_role,
            "profile_info": "unknown",
            "profile_img": "assets/img/users/users.png",
            "email": email,
            "country": "unknown",
            "no_hp": "unknown",
            "address": "unknown",
            "maps": "unknown",
            "profile_img_bg": "assets/img/bgusers/bg_users.jpg",
            "date": time_str 

        }

        db.users.insert_one(doc)
        return redirect(url_for('auth.login'))

    return render_template("auth/register.html", form=form, role=role)


@auth_bp.route("/login", methods=['POST', 'GET'])
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
                "password": pw_hash,
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
                return jsonify({"result": "fail", "msg": "We could not find a user with that id/password combination"})
            else:
                # Assuming you are using Flask's flash messages
                msg = "Invalid username or password"
                return redirect(url_for("auth.login", msg=msg))
    else:
        return render_template("auth/login.html", form=form)