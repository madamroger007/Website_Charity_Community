from flask import Flask, render_template,jsonify,redirect,request,url_for
app = Flask(__name__)

#************************* Login & Register client || admin *****************************
@app.route("/login")
def login():
    return render_template("auth/login.html")

@app.route("/register/<role>")
def register(role):
    return render_template("auth/register.html")

#**************************************** Client ****************************************
@app.route('/')
def index():
    return render_template('client/index.html')

@app.route('/about')
def about():
    return render_template('client/about.html')

@app.route('/news')
def news():
    return render_template('client/news.html')

@app.route('/donate')
def donate():
    return render_template('client/donate.html')

@app.route('/donate/payment')
def donate_pay():
    return render_template('client/payment.html')

@app.route('/project')
def project():
    return render_template('client/project.html')

@app.route('/contact_us')
def contact_us():
    return render_template('client/contact.html')

@app.route('/profile')
def profile():
    return render_template('client/profile.html')

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
    app.run(host='127.0.0.1', port=8000, debug=True)
 