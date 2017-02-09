from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

DATABASE_URL_MY = 'postgres://eadumqulgsrlui:92584b3b650cda384c3aabf71d4bd8d990f356962074d8d05a94cea9c4ec6108@ec2-107-20-230-243.compute-1.amazonaws.com:5432/ddjhqjtepf5ofe?sslmode=require'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL_MY
mydb = SQLAlchemy(app)

class Data(mydb.Model):
    __tablename__ = "data"
    id = mydb.Column(mydb.Integer,primary_key=True)
    email = mydb.Column(mydb.String(120),unique=True)
    user_name = mydb.Column(mydb.String(50),unique=True)
    user_rating = mydb.Column(mydb.Integer)

    def __init__(self,email,user_name,user_rating):
        self.email = email
        self.user_name = user_name
        self.user_rating = user_rating

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/success/",methods=["POST"])
def success():
    if request.method == 'POST':
        email = request.form['email_name']
        user_name = request.form['user_name']
        user_rating = request.form['user_rating']
        if mydb.session.query(Data).filter(Data.email == email).count() == 0:
            data = Data(email,user_name,user_rating)
            mydb.session.add(data)
            mydb.session.commit()
            average_rating = mydb.session.query(func.avg(Data.user_rating)).scalar()
            count = mydb.session.query(Data.email).count()
            return render_template('success.html',average_rating=average_rating,user_name=user_name,
            user_rating=user_rating,count=count)
        return render_template('index.html',
        text="Seems like you have already gave your views.. Try a new email :)")

if __name__ == "__main__":
    app.debug = True
    app.run()
