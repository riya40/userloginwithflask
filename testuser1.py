from flask import jsonify
from flask import request
from flask import Flask
from flask_mail import Mail, Message
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from pymongo import MongoClient

# configure te database
client = MongoClient('mongodb://localhost:27017/')
db = client["databse"]
user = db["User"]
app = Flask(__name__)
jwt = JWTManager(app)

# configure the smtp mail
app.config["JWT_SECRET_KEY"] = "riyasecretkey"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tripuranunna10@gmail.com'
app.config['MAIL_PASSWORD'] = 'Priyanka@20'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/register/", methods=["POST"])
def register():
    """
    in the database its checks the user is already registered or not
    if not it can register to the account
    """
    email = request.form["email"]
    test = user.find_one({"email": email})
    if test:
        return jsonify(message="already exist"), 409
    else:
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        password = request.form["password"]
        user_info = dict(firstname=firstname, lastname=lastname, email=email, password=password)
        user.insert_one(user_info)
        return jsonify(message="user added successfull")


@app.route("/login", methods=["POST"])
def login():
    """
    it returns the user is already  registered and checks the username and password
    if username and password matches it generates the token for access
    """
    if request.is_json:
        email = request.json.get["email"]
        password = request.json.get["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    test = user.find_one({"email": email, "password": password})
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


@app.route("/mail")
def index():
    """
    Sending the email to the registered email account for the activation
    """
    msg = Message(
        'Hello',
        sender='tripuranunna10@gmail.com',
        recipients=['receiver’priyanunna20@gmail.com']
    )
    msg.body = 'Hello Flask message sent from Flask-Mail'.encode('utf-8')
    mail.send(msg)
    return 'Sent'


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
