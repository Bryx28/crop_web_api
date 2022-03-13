from flask import Flask, jsonify, request
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc
import datetime, random, psycopg2
from datetime import timezone, timedelta
import psycopg2.extras
from converter import date_to_words, number_formatting

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kwqxcelviwbiyf:570b87e2f2fa138774cb2df0572e7359316ea44c17be8d7dcfe56192724c8f45@ec2-3-211-228-251.compute-1.amazonaws.com:5432/dfqt1p61srvec0'
app.config['SECRET_KEY'] = 'tH3s3iS@s3cr3tk3Y'

db = SQLAlchemy(app)
ma = Marshmallow(app)

def db_connection():
    try:
        conn = psycopg2.connect(
                host='ec2-3-211-228-251.compute-1.amazonaws.com',
                database='dfqt1p61srvec0',
                user='kwqxcelviwbiyf',
                password='570b87e2f2fa138774cb2df0572e7359316ea44c17be8d7dcfe56192724c8f45'
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
    nitrogen_content = db.Column(db.Integer, nullable=False)
    phosphorous_content = db.Column(db.Integer, nullable=False)
    potassium_content = db.Column(db.Integer, nullable=False)
    ph_level_content = db.Column(db.Float, nullable=False)

db.create_all()

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

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
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
        device_num = request.json.get('device_number')
        nitrogen_content = request.json.get('nitrogen')
        phosphorous_content = request.json.get('phosphorous')
        potassium_content = request.json.get('potassium')
        ph_level_content = request.json.get('ph_level')
        recommended_crop = random.choice(['Rice', 'Maize', 'Corn', 'Banana', 'Watermelon'])

        new_prediction = Recommendations(date=current_date,
                                         device_number=device_num,
                                         recommended = recommended_crop,
                                         nitrogen_content=nitrogen_content,
                                         phosphorous_content=phosphorous_content,
                                         potassium_content=potassium_content,
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

@app.route('/existing_username/<username>', methods=['GET'])
def existing_username(username):
    conn = db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM public.\"user\" WHERE username='{}'".format(username))
    exist = cursor.fetchone()
    user = user_schema.dump(exist)
    return user_schema.jsonify(user)

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
    updated_title = request.json.get('title')
    updated_content  = request.json.get('content')

    update_query = """ UPDATE public."post"
                        SET title='{}',
                            content='{}'
                        WHERE id={}"""

    cursor.execute(update_query.format(updated_title,
                                       updated_content,
                                       post_id))
    
    conn.commit()

    cursor.execute("SELECT * FROM public.\"post\" WHERE id={}".format(post_id))
    post = cursor.fetchone()

    return post_schema.jsonify(post)

if __name__ == "__main__":
    app.run()