from pymongo import MongoClient
import jwt
from datetime import datetime
import os
from flask import jsonify, request, redirect, url_for,Blueprint
from validation.forms import Newsform,UpdateProjectsform, UpdateNewsform,Projectsform,UpdateUsersForm
from bson import ObjectId


api_bp = Blueprint('api', __name__)
SECRET_KEY=os.environ.get("SECRET_KEY")
MONGODB_URI=os.environ.get("MONGODB_URI")
DB_NAME=os.environ.get("DB_NAME")
TOKEN_KEY=os.environ.get("TOKEN_KEY")


client = MongoClient(MONGODB_URI)
db = client[DB_NAME]



#************* Function Helper
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


#****************************************** GET API ******************************************

#***************** USERS

@api_bp.route('/get_users')
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
        "users": user_list,

    })


#***************** NEWS

@api_bp.route('/get_news')
def get_news():
    news = db.news.find({}).sort('date', -1).limit(20)
  
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
        "news": news_list,
      
    })

@api_bp.route('/get_news/<newsId>')
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


#***************** DONATE

@api_bp.route('/get_donate')
def get_donate():
    donate = db.donations.find({}).sort('date', -1).limit(20)
    donate_list = [
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
        for user in donate
    ]

    return jsonify({
        "msg": "success",
        "donation": donate_list,

    })


#***************** PROJECTS

@api_bp.route('/get_project')
def get_project():
    projects = db.projects.find({}).sort('date', -1).limit(20)
    projects_list = [
        {
            '_id': str(user['_id']),
            'username': user.get('username', ''),
            'title': user.get('title', ''),
            'img': user.get('img', ''),
            'description': user.get('description', ''),
            'topic': user.get('topic', ''),
            'date': user.get('date', ''),
        }
        for user in projects
    ]

    return jsonify({
        "msg": "success",
        "projects": projects_list
    })

@api_bp.route('/get_project/<projectId>')
def get_projectId(projectId):
    projects = db.projects.find_one({'_id':ObjectId(projectId)})
    projects_list =  {
            '_id': str(projects['_id']),
            'username': projects.get('username', ''),
            'title': projects.get('title', ''),
            'img': projects.get('img', ''),
            'description': projects.get('description', ''),
            'topic': projects.get('topic', ''),
            'date': projects.get('date', ''),
        }


    return jsonify({
        "msg": "success",
        "projects": projects_list
    })



#***************** Total All

@api_bp.route('/get_total')
def get_total():
    # total user
    total_user = db.users.count_documents({})
    # total news
    total_news = db.news.count_documents({})
    # total project
    total_projects = db.projects.count_documents({})  
    # total donation
    pipeline = [
        {
            '$group': {
                '_id': None,
                'total_donation_amount': {'$sum': '$donation_amount'}
            }
        }
    ]      
    result = list(db.donations.aggregate(pipeline))

    # Total user donasi
    user_donate = db.donations.count_documents({})
    
    # Function to get the latest date from a collection
    def get_latest_timestamp(collection):
        latest_data = collection.find_one(sort=[("date", -1)])
        return latest_data.get("date")



    # Get the latest timestamps for each collection
    timestamp_users = get_latest_timestamp(db.users)
    timestamp_news = get_latest_timestamp(db.news)
    timestamp_projects = get_latest_timestamp(db.projects)
    timestamp_donations = get_latest_timestamp(db.donations)

    return jsonify({
        "msg": "success",
        "total_users": total_user,
        "total_news": total_news,
        "total_donation": result[0]['total_donation_amount'],
        "user_donate": user_donate,
        "total_project": total_projects,
        "timestamp_users": timestamp_users,
        "timestamp_news": timestamp_news,
        "timestamp_projects": timestamp_projects,
        "timestamp_donations": timestamp_donations
    })


#***************** Contact 
@api_bp.route('/get_contact')
def get_contact():
    
    contact = db.message.find({}).sort('date', -1).limit(20)
    
    
    contact_list = [
        {
            '_id': str(user['_id']),
            'username': user.get('username', ''),
            'name': user.get('name', ''),
            'email': user.get('email', ''),
            'message': user.get('message', ''),
            'phone': user.get('phone', ''),
            'img': user.get('img', ''),
            'date': user.get('date', ''),
        }
        for user in contact
    ]

    return jsonify({
        "msg": "success",
        "contacs": contact_list,
      
    })

#****************************************** POST API ********************************************* 

#***************** NEWS

@api_bp.route("/posting_news", methods=["POST"])
def posting_news():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        if not user_info:
            return jsonify({"result": "error", "msg": "User not found"})
        form = Newsform()
        file = request.files.get('img_give')
        if form.validate():
            title_receive = form.title_give.data
            description_receive = form.description_give.data
            topic_receive = form.topic_give.data
            # time
            time_now = datetime.utcnow()
            time_str = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

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

            return jsonify({"result": "success", "msg": "Posting News Successful"})
        else:
            # Handle the case when form validation fails
            errors = {field: form[field].errors for field in form.errors}
            return jsonify({"result": "error", "msg": "Form validation failed", "errors": errors})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))

#***************** PROJECTS

@api_bp.route("/posting_project", methods=["POST"])
def posting_project():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        if not user_info:
            return jsonify({"result": "error", "msg": "User not found"})
        form = Projectsform()
        
        if form.validate():
            title_receive = form.title_give.data
            description_receive = form.description_give.data
            topic_receive = form.topic_give.data
            file = request.files.get('img_give')
            # time
            time_now = datetime.utcnow()
            time_str = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            # Simpan gambar ke server
            img_url = save_image(file, 'projects')

            doc = {
                "username": user_info.get("username"),
                "title": title_receive,
                "img": img_url,
                "description": description_receive,
                "topic": topic_receive,
                'date': time_str
            }

            db.projects.insert_one(doc)

            return jsonify({"result": "success", "msg": "Posting Projects Successful"})
        else:
            # Handle the case when form validation fails
            errors = {field: form[field].errors for field in form.errors}
            return jsonify({"result": "error", "msg": "Form validation failed", "errors": errors})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))

#**************** Contact
@api_bp.route("/posting_contact", methods=["POST"])
def posting_contact():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        if not user_info:
            return jsonify({"result": "error", "msg": "User not found"})
          
        name_receive = request.form.get("name_give")
        email_receive = request.form.get("email_give")
        message_receive = request.form.get('message_give') 
        phone_receive = request.form.get("phone_give") 
        # time
        print(name_receive)
        print(email_receive)
        print(message_receive)
        print(phone_receive)

        time_now = datetime.utcnow()
        time_str = time_now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        doc = {
                "username": user_info.get("username"),
                "name": name_receive,
                "email": email_receive,
                "message": message_receive,
                "phone": phone_receive,
                "img": user_info.get("profile_img"),
                'date': time_str
            }

        db.message.insert_one(doc)
        return jsonify({"result": "success", "msg": "Posting Message Successful"})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))

#****************************************** UPDATE API ******************************************

#***************** USERS

@api_bp.route("/update_users/<userid>", methods=["POST"])
def update_users(userid):
    token_receive = request.cookies.get(TOKEN_KEY)
    print(userid)
    form = UpdateUsersForm()  # Gunakan UpdateUsersForm, bukan UpdateNewsform
    try:
        payload = decode_token(token_receive)
        username = payload.get("username")
        if form.validate():
            fullname_receive = form.fullname_receive.data
            profile_info_receive = request.form.get("profile_info_receive")
            email_receive = form.email_receive.data
            maps_receive = request.form.get("maps_receive")
            no_hp_receive = form.no_hp_receive.data
            address_receive = request.form.get("address_receive")
            country_receive = form.country_receive.data

            new_doc = {
                "fullname": fullname_receive,
                "profile_info": profile_info_receive,
                "email": email_receive,
                "maps": maps_receive,
                "no_hp": no_hp_receive,
                "address": address_receive,
                "country": country_receive
            }

            # Check if a new image is uploaded
            if "profile_img_receive" in request.files:
                file = request.files.get('profile_img_receive')

                # Check if the file is not empty
                if file and file.filename:
                    img_url = save_image(file, 'users')
                    new_doc["profile_img"] = img_url
                else:
                    # Handle the case when the file is empty
                    return jsonify({"result": "error", "msg": "No file provided for update"})
            elif "profile_bg_img_receive" in request.files:
                file = request.files.get('profile_bg_img_receive')

                # Check if the file is not empty
                if file and file.filename:
                    img_url = save_image(file, 'bgusers')
                    new_doc["profile_img_bg"] = img_url
                else:
                    # Handle the case when the file is empty
                    return jsonify({"result": "error", "msg": "No file provided for update"})
            # Update other fields
            db.users.update_one({"_id": ObjectId(userid)}, {"$set": new_doc})

            return jsonify({"result": "success", "msg": "Update Successful"})
        else:
            # Handle the case when form validation fails
            errors = {field: form[field].errors for field in form.errors}
            return jsonify({"result": "error", "msg": "Form validation failed", "errors": errors})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))



#***************** NEWS

@api_bp.route("/update_news/<newsid>", methods=["POST"])
def update_news(newsid):
    token_receive = request.cookies.get(TOKEN_KEY)
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
                    db.news.update_one({"_id": ObjectId(newsid)}, {"$set":  new_doc })
                    return jsonify({"result": "error", "msg": "No file provided for update"})
            # Update other fields
            db.news.update_one({"_id": ObjectId(newsid)}, {"$set":  new_doc })
            print("berhasil")

            return jsonify({"result": "success", "msg": "Update Successful"})
        else:
            # Handle the case when form validation fails
            errors = {field: form[field].errors for field in form.errors}
            return jsonify({"result": "error", "msg": "Form validation failed", "errors": errors})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


#***************** PROJECTS
@api_bp.route("/update_project/<projectid>", methods=["POST"])
def update_project(projectid):
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        username = payload.get("username")
        form = UpdateProjectsform()
        print(form.validate())
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
                    img_url = save_image(file, 'projects')
                    new_doc["img"] = img_url
                else:
                    # Handle the case when the file is empty
                    db.projects.update_one({"_id": ObjectId(projectid)}, {"$set":  new_doc })
                    return jsonify({"result": "error", "msg": "No file provided for update"})
            # Update other fields
            db.projects.update_one({"_id": ObjectId(projectid)}, {"$set":  new_doc })

            return jsonify({"result": "success", "msg": "Update Successful"})
        else:
            # Handle the case when form validation fails
            errors = {field: form[field].errors for field in form.errors}
            return jsonify({"result": "error", "msg": "Form validation failed", "errors": errors})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


#****************************************** DELETE API ******************************************

#***************** USERS

@api_bp.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    result = db.users.delete_one({'_id': ObjectId(user_id)})
    response = {
        'status': 'success' if result.deleted_count == 1 else 'error',
        'message': 'User deleted successfully' if result.deleted_count == 1 else 'User not found or could not be deleted'
    }
    return jsonify(response)

#***************** NEWS

@api_bp.route('/delete_news/<news_id>', methods=['POST'])
def delete_news(news_id):
    result = db.news.delete_one({'_id': ObjectId(news_id)})
    response = {
        'status': 'success' if result.deleted_count == 1 else 'error',
        'message': 'News deleted successfully' if result.deleted_count == 1 else 'News not found or could not be deleted'
    }
    return jsonify(response)

#***************** PROJECTS

@api_bp.route('/delete_project/<project_id>', methods=['POST'])
def delete_project(project_id):
    result = db.projects.delete_one({'_id': ObjectId(project_id)})
    response = {
        'status': 'success' if result.deleted_count == 1 else 'error',
        'message': 'Projects deleted successfully' if result.deleted_count == 1 else 'Projects not found or could not be deleted'
    }
    return jsonify(response)

#**************** Contact
@api_bp.route('/delete_contact/<contact_id>', methods=['POST'])
def delete_contact(contact_id):
    result = db.message.delete_one({'_id': ObjectId(contact_id)})
    response = {
        'status': 'success' if result.deleted_count == 1 else 'error',
        'message': 'Projects deleted successfully' if result.deleted_count == 1 else 'Projects not found or could not be deleted'
    }
    return jsonify(response)