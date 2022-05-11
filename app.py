from flask import Flask, jsonify, request
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy import desc
from datetime import timezone, timedelta
from converter import *
from keras.models import load_model
from decouple import config
import datetime, random, psycopg2
import psycopg2.extras
import warnings
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['ALLOW_PRIVATE_REPOS'] = True
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

def db_connection():
    try:
        conn = psycopg2.connect(
                host= config('HOST'),
                database= config('DATABASE'),
                user= config('USER'),
                password= config('PASSWORD')
                )
    except psycopg2.Error as e:
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
    author = db.relationship("Post", backref="author", lazy=True)

    def  __repr__(self):
        return f"User({self.username} - {self.user_fname} {self.user_lname})"

    def get_object(self):
        data = {
                    "user_id": self.user_id,
                    "user_image": self.user_image,
                    "user_fname": self.user_fname,
                    "user_mname": self.user_mname,
                    "user_lname": self.user_lname,
                    "username": self.username,
                    "email": self.email
               }
        return data

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    def get_object(self):
        data = {
                    "id": self.id,
                    "title": self.title,
                    "date_posted": self.date_posted,
                    "content": self.content,
                    "user_id": self.user_id,
                    "author": self.author.get_object()
               }
        return data

class Recommendations(db.Model):
    __tablename__ = "recommendations"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    device_number = db.Column(db.String(20), nullable=False)
    recommended = db.Column(db.String(50), nullable=False)
    nitrogen_content = db.Column(db.String(50), nullable=False)
    phosphorous_content = db.Column(db.String(50), nullable=False)
    potassium_content = db.Column(db.String(50), nullable=False)
    ph_level_content = db.Column(db.Float, nullable=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "user_image", "user_fname", "user_mname", 
                "user_lname", "username", "email", "password")

class RecommendationSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "device_number", "recommended",
                    "nitrogen_content", "phosphorous_content",
                    "potassium_content", "ph_level_content")

class UserPostSchema(ma.Schema):
    class Meta:
        fields = ("user_id", "user_image", "username")

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "date_posted", "content", "")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

crop_schema = RecommendationSchema()
crops_schema = RecommendationSchema(many=True)

user_post_schema = UserPostSchema()
user_posts_schema = UserPostSchema(many=True)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

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

@app.route('/create_mobile', methods=['POST'])
def create_mobile():
    args = request.args
    user_fname = args.get('user_fname')
    user_mname = args.get('user_mname')
    user_lname = args.get('user_lname')
    username = args.get('username')
    email = args.get('email')
    password = args.get('password')

    new_user = User(user_fname = user_fname, 
                    user_mname = user_mname, 
                    user_lname = user_lname,
                    username = username,
                    email = email,
                    password = password)
    
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route("/encrypt_pass", methods=['GET'])
def encrpyt_pass():
    args = request.args
    unencrypted = args.get('password')
    hashed_pw = bcrypt.generate_password_hash(unencrypted).decode('utf-8')
    encrypted = {
                    "hashed_pass":hashed_pw
                }
    return jsonify(encrypted)

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        #Row Counter
        cursor.execute("SELECT COUNT(*) FROM public.\"recommendations\"")
        x = cursor.fetchone()
        conn.commit()
        if x[0] > 15:
            cursor.execute("DELETE FROM public.\"recommendations\"")
            conn.commit()
        now = datetime.datetime.now(timezone(timedelta(hours=8)))
        word_month, str_day = date_to_words(now.month, now.day)
        str_hour = number_formatting(now.hour)
        str_minute = number_formatting(now.minute)
        str_sec = number_formatting(now.second)
        current_date = """{} {}, {} {}:{}:{}""".format(word_month,
                                                      str_day,
                                                      now.year,
                                                      str_hour,
                                                      str_minute,
                                                      str_sec)
        device_num = request.json.get('dev_num')
        nitrogen_content = request.json.get('n')
        phosphorous_content = request.json.get('p')
        potassium_content = request.json.get('k')
        lat = request.json.get('lat')
        lon = request.json.get('long')
        temperature, humidity = current_weather(str(lat), str(lon))
        ph_level_content = request.json.get('ph')

        #Rainfall in mm for the last 28 days (1 Month)
        rain_list = []
        scopes = ((27, 21), (20, 14), (13, 7), (6, 0))
        for scope in scopes:
            end_date = datetime.datetime.now() - datetime.timedelta(scope[1])
            end = str(int(end_date.timestamp()))
            start_date = datetime.datetime.now() - datetime.timedelta(scope[0])
            start = str(int(start_date.timestamp()))
            rain_list.append(history_weather(str(lat), str(lon), start, end))
        rainfall = 0
        for a in rain_list:
            rainfall += sum(a)
        model = load_model('lstm_model.h5')
        input_df = pd.DataFrame({'N': [nitrogen_content],
                         'P': [phosphorous_content],
                         'K': [potassium_content],
                         'temperature': [temperature],
                         'humidity': [humidity],
                         'ph': [ph_level_content],
                         'rainfall': [rainfall]})
        result = model.predict(input_df)
        crops = recommended_crops(result)
        nitrogen_desc = nitrogen_descriptive(nitrogen_content)
        phosphorous_desc = phosphorous_descriptive(phosphorous_content)
        potassium_desc = potassium_descriptive(potassium_content)
        new_prediction = Recommendations(date=current_date,
                                         device_number=device_num,
                                         recommended = crops,
                                         nitrogen_content=nitrogen_desc,
                                         phosphorous_content=phosphorous_desc,
                                         potassium_content=potassium_desc,
                                         ph_level_content=ph_level_content)

        db.session.add(new_prediction)
        db.session.commit()
        return crop_schema.jsonify(new_prediction)
    
    if request.method == "GET":
        table_recommendation = []
        cursor.execute("SELECT * FROM public.\"recommendations\" ORDER BY id DESC")
        for a in cursor.fetchall():
             table_recommendation.append(a)
        if table_recommendation is not None:
            return crops_schema.jsonify(table_recommendation)
        else:
            return crop_schema.jsonify()

@app.route('/dash_info', methods=['GET'])
def dash_info():
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT recommended FROM public.\"recommendations\"")
    crops = cursor.fetchall()
    crop_list = [x[0] for x in crops]
    all_crops = [x[0] for x in crops.split(',')]
    count = [0 for x in range(len(crop_list))]
    crop_dict = dict(zip(crop_list, count))

    crop_dict_res = crop_counter(all_crops, crop_dict)
    return jsonify(crop_dict_res)

@app.route('/new_post', methods=['POST'])
def new_post():
    now = datetime.datetime.now(timezone(timedelta(hours=8)))
    word_month, str_day = date_to_words(now.month, now.day)
    str_hour = number_formatting(now.hour)
    str_minute = number_formatting(now.minute)
    str_sec = number_formatting(now.second)
    current_date = """{} {}, {} {}:{}:{}""".format(word_month,
                                                  str_day,
                                                  now.year,
                                                  str_hour,
                                                  str_minute,
                                                  str_sec)
    title = request.json.get('title')
    content = request.json.get('content')
    user = request.json.get('author')
    
    new_post_created = Post(title = title, 
                            content = content,
                            date_posted = current_date,
                            user_id = user)
    
    db.session.add(new_post_created)
    db.session.commit()
    return post_schema.jsonify(new_post_created) 

@app.route('/get_posts', methods=['GET'])
def get_posts():
    posts = []
    data = Post.query.all()
    for index in range(len(data)):
        posts.append(data[-1-index].get_object())
    if posts is not None:
        return jsonify(posts)
    else:
        return post_schema.jsonify()

@app.route('/post/<post_id>', methods=['GET'])
def get_post(post_id):
    data = Post.query.get_or_404(post_id)
    if data is not None:
        return jsonify(data.get_object())
    else:
        return post_schema.jsonify()

@app.route("/existing_username", methods=['GET'])
def existing_username():
    args = request.args
    username = args.get("username")
    print(username)
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM public.\"user\" WHERE username='{}'".format(username))
    exist = cursor.fetchone()
    user = user_schema.dump(exist)
    return user_schema.jsonify(user)

@app.route("/validate_pass", methods=['GET'])
def validate_pass():
    args = request.args
    encrpyted = args.get("encrypted")
    password = args.get("password")
    if bcrypt.check_password_hash(encrpyted, password):
        access = {
                    "access_granted": 1
                }
    else:
        access = {
                    "access_granted": 0
                }
    return jsonify(access)

@app.route('/existing_email/<email>', methods=['GET'])
def existing_email(email):
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM public.\"user\" WHERE email='{}'".format(email))
    exist = cursor.fetchone()
    user = user_schema.dump(exist)
    return user_schema.jsonify(user)

@app.route('/load_user/<user_id>', methods=['GET'])
def load_user(user_id):
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM public.\"user\" WHERE user_id={}".format(user_id))
    exist = cursor.fetchone()
    user  = user_schema.dump(exist)
    return user_schema.jsonify(user)

@app.route('/update_account/<user_id>', methods=['PUT'])
def update_account(user_id):
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    user_image = request.json.get('user_image')
    user_fname = request.json.get('user_fname')
    user_mname = request.json.get('user_mname')
    user_lname = request.json.get('user_lname')
    username = request.json.get('username')
    email = request.json.get('email')
    
    update_query = """ UPDATE public."user"
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

    cursor.execute("SELECT * FROM public.\"user\" WHERE user_id={}".format(user_id))
    account = cursor.fetchone()

    return user_schema.jsonify(account)

@app.route('/update_post/<post_id>', methods=['PUT'])
def update_post(post_id):
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    now = datetime.datetime.now(timezone(timedelta(hours=8)))
    word_month, str_day = date_to_words(now.month, now.day)
    str_hour = number_formatting(now.hour)
    str_minute = number_formatting(now.minute)
    str_sec = number_formatting(now.second)
    current_date = """{} {}, {} {}:{}:{}""".format(word_month,
                                                  str_day,
                                                  now.year,
                                                  str_hour,
                                                  str_minute,
                                                  str_sec)
    
    updated_title = request.json.get('title')
    updated_content  = request.json.get('content')

    update_query = """ UPDATE public."post"
                        SET title='{}',
                            content='{}',
                            date_posted='{}'
                        WHERE id={}"""

    cursor.execute(update_query.format(updated_title,
                                       updated_content,
                                       current_date,
                                       post_id))
    
    conn.commit()

    cursor.execute("SELECT * FROM public.\"post\" WHERE id={}".format(post_id))
    post = cursor.fetchone()

    return post_schema.jsonify(post)

@app.route('/delete_post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute(f"DELETE FROM public.\"post\" WHERE id={post_id}")
    conn.commit()
    
    return post_schema.jsonify()

if __name__ == "__main__":
    warnings.simplefilter('ignore')
    app.run()