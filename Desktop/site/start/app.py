from crypt import methods
from turtle import title
from flask import Flask, redirect, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class A(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<A %r>' % self.id

@app.route('/')
@app.route('/home')
def index():
   return render_template("index.html")

@app.route('/about')
def about():
   return render_template("about.html")


@app.route('/post')
def post():
    a = A.query.order_by(A.date.desc()).all()
    return render_template("post.html", a=a)

@app.route('/post/<int:id>')
def post_id(id):
    a = A.query.get(id)
    return render_template("post_id.html", a=a)

@app.route('/post/<int:id>/del')
def post_delete(id):
    a = A.query.get_or_404(id)

    try:
        db.session.delete(a)
        db.session.commit()
        return redirect('/post')
    except:
        return "При удалении статьи произошла ошибка"

@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    a = A.query.get(id)
    if request.method == "POST":
        a.title = request.form['title']
        a.intro = request.form['intro']
        a.text = request.form['text'] 

        try:
           db.session.commit()
           return redirect('/post') 
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("update.html", a=a)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        a = A(title=title, intro=intro, text=text)

        try:
           db.session.add(a)
           db.session.commit()
           return redirect('/post') 
        except:
            return "При добовлении статьи произошла ошибка"
    else:
        return render_template("create.html")
