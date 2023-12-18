from pymongo import MongoClient
import jwt
from datetime import datetime
import os
from flask import render_template, request, redirect, url_for,Blueprint
from validation.forms import DonateForm,UpdateUsersForm
import json
from bson import ObjectId

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
        msg = request.args.get("msg","")   
        print(msg)
       # Replace single quotes with double quotes and then parse as JSON
        if msg != "":
            msg_str = msg.replace("'", "\"")
            msg_object = json.loads(msg_str)
                   
            return render_template('client/donate.html', user_info=user_info, msg=msg_object)
        return render_template('client/donate.html', user_info=user_info,msg=msg)
     
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

            db.donations.insert_one(donation_data)
            msg = {"status": 201, "msg":"Terima Kasih sudah donasi"}
            return redirect(url_for('client.donate',msg=msg))
        elif request.method == 'POST' and not form.validate():
            # Pesan gagal registrasi jika data dari form tidak sesuai
            msg = {"status": 400, "msg": "Data tidak sesuai, silahkan cek kembali"}
            return render_template('client/payment.html', user_info=user_info, form=form, msg=msg)
        else:
            # Pesan gagal registrasi jika data dari form tidak sesuai
            msg= "Mari kita donasi"
            return render_template('client/payment.html', user_info=user_info, form=form,msg=msg)
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
       
        return render_template('client/contact.html', user_info=user_info)
       
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@client_bp.route('/profile')
def profile():
    token_receive = request.cookies.get(TOKEN_KEY)
    form = UpdateUsersForm()
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        # Konversi ObjectId menjadi string
        user_info["_id"] = str(user_info["_id"])
       
        return render_template('client/profile.html', user_info=user_info,form=form)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))

@client_bp.route('/detail/<id>', methods=["POST", "GET"])
def detail(id):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        # Try finding the document in the 'news' collection
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        news = db.news.find_one({'_id': ObjectId(id)})
        if news:
            page ="news"
            news['date'] = datetime.strptime(news['date'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%d %B %Y')
            return render_template('client/detail.html', detail=news, user_info=user_info,page=page)
        # If not found in 'news', try finding in the 'projects' collection
        project = db.projects.find_one({'_id': ObjectId(id)})
        if project:
            project['date'] =  datetime.strptime(project['date'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%d %B %Y')
            page="project"
            return render_template('client/detail.html', detail=project,user_info=user_info,page=page)
        
        # If not found in either collection, display a message
        msg = "Tidak ada"
        page=""
        return render_template('client/detail.html', detail=msg,user_info=user_info,page=page)
    
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))