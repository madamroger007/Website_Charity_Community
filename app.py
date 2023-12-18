from dotenv import load_dotenv
from os.path import join, dirname
import os
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from routes import auth_bp,admin_bp,api_bp,client_bp



# ************************* Variable & Key *****************************
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


# * config flask
app = Flask(__name__, template_folder='templates')
csrf = CSRFProtect(app)

app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    TEMPLATE_AUTO_RELOAD=True,
    UPLOAD_FOLDER=["./static/assets/img/news",
                   "./static/assets/img/projects", "./static/assets/img/users"],
)

# * Connect database

app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)



# *********************************************** Error Page *********************************************

# Handler untuk kesalahan server internal (404)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

# Handler untuk kesalahan server internal (500)
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
