from pymongo import MongoClient
import jwt
from datetime import datetime
import os
from flask import render_template, request, redirect, url_for,Blueprint
from validation.forms import DonateForm,UpdateUsersForm


client_bp = Blueprint('client', __name__)

#*************** Key Config
SECRET_KEY=os.environ.get("SECRET_KEY")
MONGODB_URI=os.environ.get("MONGODB_URI")
DB_NAME=os.environ.get("DB_NAME")
TOKEN_KEY=os.environ.get("TOKEN_KEY")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]


# * Function Helper
def decode_token(payload):
    token = jwt.decode(payload, SECRET_KEY, algorithms=["HS256"])
    return token


def encode_token(payload):
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def save_image(file, file_type):
    time_now = datetime.now()
    time_str = time_now.strftime("%Y-%m-%d-%H-%M-%S")

    extention = file.filename.split(".")[-1]
    filename = f"assets/img/{file_type}/post-{time_str}.{extention}"
    file.save("./static/" +filename)

    return filename



# **************************************** Client ****************************************


@client_bp.route('/')
def index():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        if user_info["role"] == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('client/index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        msg = "Your token has expired"
        return redirect(url_for("auth.login", msg=msg))
    except jwt.exceptions.DecodeError:
        msg = "There was a problem logging your in"
        return redirect(url_for("auth.login", msg=msg))


@client_bp.route('/about')
def about():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        
        return render_template('client/about.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@client_bp.route('/news')
def news():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        
        return render_template('client/news.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@client_bp.route('/donate')
def donate():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        return render_template('client/donate.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@client_bp.route('/donate/payment',  methods=['POST', 'GET'])
def donate_pay():
    token_receive = request.cookies.get(TOKEN_KEY)
    form = DonateForm()
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
    

        if request.method == 'POST' and form.validate_on_submit():
            # time
            time_now = datetime.utcnow()
            time_str = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            # Handle the form submission, store data in MongoDB
            donation_data = {
                "username": user_info.get("username"),
                "country": form.country_give.data,
                "donation_amount": form.donate_give.data,
                "email": form.email_give.data,
                "agree": form.agree_give.data,
                "phone": form.phone_give.data,
                "bank_account": form.rekening_give.data,
                "expiry_date": form.expiry_date_give.data,
                "security_code": form.security_code_give.data,
                "full_name": form.fullname_give.data,
                "date": time_str 
            }

        # Insert the data into the MongoDB collection (adjust collection name as needed)
            db.donations.insert_one(donation_data)
            return redirect(url_for('client.donate'))

        return render_template('client/payment.html', user_info=user_info, form=form)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@client_bp.route('/project')
def project():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        return render_template('client/project.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@client_bp.route('/contact_us')
def contact_us():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        users_all = db.users.find({})
        return render_template('client/contact.html', user_info=user_info, users_all=users_all)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@client_bp.route('/profile')
def profile():
    token_receive = request.cookies.get(TOKEN_KEY)
    form = UpdateUsersForm()
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        
        return render_template('client/profile.html', user_info=user_info,form=form)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))
