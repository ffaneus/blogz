from flask import Flask, render_template, request, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import validators
import os


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:YES@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(500))
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user', lazy=True))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def create_post(self):
        post = Post(title=self.title,body=self.body)
        db.session.add(post)
        db.session.commit()

    def __repr__(self):
        return '<Post %r>' % self.title


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_user(self):
        user = User(username=self.username,password=self.password)
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/add', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user = User.query.filter_by(id=session.get('user_id'))
        if validators.valid_entry(title, body):
            new_post = Post(title=title, body=body, )
            new_post.create_post()
            return redirect('/')
    else:
        return render_template('add.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and (password == user.password):
        session.permanent = True
        session['user_authenticated'] = True
        session['user'] = user.username
        session['user_id'] = user.id
        return redirect('/')
    else:
        return render_template('login.html')

def logout():
    session['user_authenticated'] = False
    session.pop('user')
    session.pop('user_id')
    return redirect('/')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    password1 = request.form.get('password1')
    print(username)
    print(email)
    print(password)
    print(password1)
    user = User.query.filter_by(username=username).first()
    if user:
        print(user)
    else:
        new_user = User(username=username, password=password)
        new_user.create_user()
    return redirect('/')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('post.html', post=post)


@app.route('/')
def index():
    session['user'] = 'Andres'
    posts = Post.query.order_by('-id')
    user_list = User.query.all()
    return render_template('index.html', posts=posts, user_list=user_list)

if __name__ == '__main__':
    app.run()