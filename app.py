from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv
from os.path import join, dirname
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from validation.forms import RegistrationForm, LoginForm, DonateForm, Newsform, UpdateNewsform
from werkzeug.utils import secure_filename
from bson import ObjectId, json_util

# ************************* Variable & Key *****************************
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


# * config flask
app = Flask(__name__, template_folder='templates')
csrf = CSRFProtect(app)

app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    MONGODB_URI=os.environ.get("MONGODB_URI"),
    DB_NAME=os.environ.get("DB_NAME"),
    TOKEN_KEY=os.environ.get("TOKEN_KEY"),
    TEMPLATE_AUTO_RELOAD=True,
    UPLOAD_FOLDER=["./static/assets/img/news",
                   "./static/assets/img/projects", "./static/assets/img/users"],
)

# * Connect database
client = MongoClient(app.config["MONGODB_URI"])
db = client[app.config["DB_NAME"]]


# * Function Helper
def decode_token(payload):
    token = jwt.decode(payload, app.config["SECRET_KEY"], algorithms=["HS256"])
    return token


def encode_token(payload):
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token


def save_image(file, file_type):
    time_now = datetime.now()
    time_str = time_now.strftime("%Y-%m-%d-%H-%M-%S")

    extention = file.filename.split(".")[-1]
    filename = f"static/assets/img/{file_type}/post-{time_str}.{extention}"
    file.save(filename)

    return filename


# ************************* Login & Register client || admin *****************************

@app.route("/register/<role>", methods=["POST", 'GET'])
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
            "country": "unknown",
            "no_hp": "unknown",
            "address": "unknown",
            "maps": "unknown",
            "profile_img_bg": "static/assets/img/users/bg/bg_users.jpg",
            "date": time_str 

        }

        db.users.insert_one(doc)
        return redirect(url_for('login'))

    return render_template("auth/register.html", form=form, role=role)


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
                return redirect(url_for("login", msg=msg))
    else:
        return render_template("auth/login.html", form=form)

# **************************************** Client ****************************************


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
            # time
            time_now = datetime.now()
            time_str = time_now.strftime("%Y-%m-%d-%H-%M-%S")
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
            return redirect(url_for('donate'))

        return render_template('client/payment.html', user_info=user_info, form=form)
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
        users_all = db.users.find({})
        return render_template('client/contact.html', user_info=user_info, users_all=users_all)
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

# *************************************** Admin *****************************************


@app.route('/dashboard/admin')
def dashboard():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(user_info)
        return render_template('admin/index.html')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


@app.route('/dashboard/admin/users')
def users_admin():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        return render_template('admin/table-users.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


@app.route('/dashboard/admin/news')
def news_admin():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    form = Newsform()
    updateform = UpdateNewsform()
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        return render_template('admin/table-news.html', user_info=user_info, form=form, updateform=updateform)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


@app.route('/dashboard/admin/project')
def project_admin():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(user_info)
        return render_template('admin/table-project.html')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


@app.route('/dashboard/admin/donate')
def donate_admin():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(user_info)
        return render_template('admin/table-donate.html')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


@app.route('/dashboard/admin/profile')
def profile_admin():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        print(user_info)
        return render_template('admin/pages-profile.html')
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))


# *********************************************** RESTAPI *********************************************

# *************** GET API
@app.route('/get_users')
def get_users():
    users = db.users.find({})
    user_list = [
        {
            '_id': str(user['_id']),
            'username': user.get('username', ''),
            'fullname': user.get('fullname', ''),
            'email': user.get('email', ''),
            'profile_info': user.get('profile_info', ''),
            'role': user.get('role', ''),
            'country': user.get('country', ''),
            'phone': user.get('phone', ''),
            'address': user.get('address', ''),
            'maps': user.get('maps', ''),
            'date': user.get('date', ''),

        }
        for user in users
    ]

    return jsonify({
        "msg": "success",
        "users": user_list
    })

# News

@app.route('/get_news')
def get_news():
    news = db.news.find({})
    news_list = [
        {
            '_id': str(user['_id']),
            'username': user.get('username', ''),
            'title': user.get('title', ''),
            'img': user.get('img', ''),
            'description': user.get('description', ''),
            'topic': user.get('topic', ''),
            'date': user.get('date', ''),
        }
        for user in news
    ]

    return jsonify({
        "msg": "success",
        "news": news_list
    })

@app.route('/get_news/<newsId>')
def get_newsId(newsId):
    news = db.news.find_one({'_id':ObjectId(newsId)})
    news_list =  {
            '_id': str(news['_id']),
            'username': news.get('username', ''),
            'title': news.get('title', ''),
            'img': news.get('img', ''),
            'description': news.get('description', ''),
            'topic': news.get('topic', ''),
            'date': news.get('date', ''),
        }


    return jsonify({
        "msg": "success",
        "news": news_list
    })

# * Donate
@app.route('/get_donate')
def get_donate():
    news = db.news.find({})
    news_list = [
        {
            '_id': str(user['_id']),
            'username': user.get('username', ''),
            'country': user.get('country', ''),
            'donation_amount': user.get('donation_amount', ''),
            'email': user.get('email', ''),
            'agree': user.get('agree', ''),
            'phone': user.get('phone', ''),
            'bank_account': user.get('bank_account', ''),
            'date': user.get('date', ''),
        }
        for user in news
    ]

    return jsonify({
        "msg": "success",
        "news": news_list
    })



# ******************* POST API


@app.route("/posting_news", methods=["POST"])
def posting_news():
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        if not user_info:
            return jsonify({"result": "error", "msg": "User not found"})
        form = Newsform()
        file = request.files.get('img_give')
        print(form.validate())
        if form.validate():
            title_receive = form.title_give.data
            description_receive = form.description_give.data
            topic_receive = form.topic_give.data
            print(topic_receive)
            # time
            time_now = datetime.now()
            time_str = time_now.strftime("%Y-%m-%d-%H-%M-%S")

            # Simpan gambar ke server
            img_url = save_image(file, 'news')

            doc = {
                "username": user_info.get("username"),
                "title": title_receive,
                "img": img_url,
                "description": description_receive,
                "topic": topic_receive,
                'date': time_str
            }

            db.news.insert_one(doc)

            return jsonify({"result": "success", "msg": "Posting Successful"})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

# ************* UPDATE API
@app.route("/update_news/<newsid>", methods=["POST"])
def update_news(newsid):
    token_receive = request.cookies.get(app.config["TOKEN_KEY"])
    print(newsid)
    try:
        payload = decode_token(token_receive)
        username = payload.get("username")
        form = UpdateNewsform()
        
       
        if form.validate():
            title_receive = form.title_update.data
            description_receive = form.description_update.data
            topic_receive = form.topic_update.data        
            new_doc = {
                "title": title_receive,
                "description": description_receive,
                "topic": topic_receive
            }
            # Check if a new image is uploaded
            if "img_update" in request.files:

                file = request.files.get('img_update')
                # Check if the file is not empty
   
                if file and file.filename:

                    img_url = save_image(file, 'news')
                    new_doc["img"] = img_url
                else:
                    # Handle the case when the file is empty
                    return jsonify({"result": "error", "msg": "No file provided for update"})
            # Update other fields
            db.news.update_one({"_id": ObjectId(newsid)}, {"$set":  new_doc })

            return jsonify({"result": "success", "msg": "Update Successful"})
        else:
            # Handle the case when form validation fails
            errors = {field: form[field].errors for field in form.errors}
            return jsonify({"result": "error", "msg": "Form validation failed", "errors": errors})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

# ****************** DELETE API
@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    result = db.users.delete_one({'_id': ObjectId(user_id)})
    response = {
        'status': 'success' if result.deleted_count == 1 else 'error',
        'message': 'User deleted successfully' if result.deleted_count == 1 else 'User not found or could not be deleted'
    }
    print("delete user")
    return jsonify(response)


@app.route('/delete_news/<news_id>', methods=['POST'])
def delete_news(news_id):
    result = db.news.delete_one({'_id': ObjectId(news_id)})
    response = {
        'status': 'success' if result.deleted_count == 1 else 'error',
        'message': 'News deleted successfully' if result.deleted_count == 1 else 'News not found or could not be deleted'
    }
    print("delete user")
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
