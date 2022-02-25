from flask import Flask, jsonify, request
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc
import pymysql


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql6475255:nYTHkyTUtR@sql6.freesqldatabase.com/sql6475255'
app.config['SECRET_KEY'] = 'secret key'

db = SQLAlchemy(app)
ma = Marshmallow(app)

def db_connection():
    try:
        conn = pymysql.connect(
            host='sql6.freesqldatabase.com',
            database='sql6475255',
            user='sql6475255',
            password='nYTHkyTUtR',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(e)
    return conn

class User(db.Model,UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    user_fname = db.Column(db.String(50), nullable=False)
    user_mname = db.Column(db.String(50), nullable=False)
    user_lname = db.Column(db.String(50))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def  __repr__(self):
        return f"User({self.username} - {self.user_fname} {self.user_lname})"

db.create_all()

class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "user_image", "user_fname", "user_mname", 
                "user_lname", "username", "email", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/create', methods=['POST'])
def create():
    user_fname = request.json.get('user_fname')
    user_mname = request.json.get('user_mname')
    user_lname = request.json.get('user_lname')
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    new_user = User(user_fname = user_fname, 
                    user_mname = user_mname, 
                    user_lname = user_lname,
                    username = username,
                    email = email,
                    password = password)
    
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/existing_username/<username>', methods=['GET'])
def existing_username(username):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username='{}'".format(username))
    exist = cursor.fetchone()
    print(exist)
    user = user_schema.dump(exist)
    return user_schema.jsonify(user)

@app.route('/existing_email/<email>', methods=['GET'])
def existing_email(email):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE email='{}'".format(email))
    exist = cursor.fetchone()
    user = user_schema.dump(exist)
    return user_schema.jsonify(user)

@app.route('/load_user/<user_id>', methods=['GET'])
def load_user(user_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE user_id={}".format(user_id))
    exist = cursor.fetchone()
    user  = user_schema.dump(exist)
    return user_schema.jsonify(user)

@app.route('/update_account/<user_id>', methods=['PUT'])
def update_account(user_id):
    conn = db_connection()
    cursor = conn.cursor()
    user_image = request.json.get('user_image')
    user_fname = request.json.get('user_fname')
    user_mname = request.json.get('user_mname')
    user_lname = request.json.get('user_lname')
    username = request.json.get('username')
    email = request.json.get('email')
    
    update_query = """ UPDATE user
                    SET user_image='{}',
                        user_fname='{}',
                        user_mname='{}',
                        user_lname='{}',
                        username='{}',
                        email='{}'
                    WHERE user_id={}"""
    
    cursor.execute(update_query.format(user_image,
                                    user_fname,
                                    user_mname,
                                    user_lname,
                                    username,
                                    email, 
                                    user_id))
    conn.commit()

    cursor.execute("SELECT * FROM user WHERE user_id={}".format(user_id))
    account = cursor.fetchone()

    return user_schema.jsonify(account)

if __name__ == "__main__":
    app.run()