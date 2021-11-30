# from flask import Flask
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()

from itertools import product
import re
from dns.message import Message
from flask import Flask,jsonify,request
from flask import render_template
from flask.json import jsonify
from nltk.util import pr
# from pymongo import message
from flask import flask_pymongo as fp
# from fp import PyMongo
import gridfs
import process1
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.aq5jb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('mongodata')
# mongo = pymongo.PyMongo(app)
mongo = fp.PyMongo(app)
fs = gridfs.GridFS(mongo.db)

# @app.route('/',methods = ['GET', 'POST'])
# def home():  # put application's code here
#     return render_template("voice.html")

@app.route('/',methods = ['GET', 'POST'])
def index():  # put application's code here
    return render_template("login.html")

@app.route('/login',methods=['GET','POST'])
def login():
    records = db.user
    username=request.form['uname']
    password=request.form['pass']
    
    user_found = records.find_one({"username": username})
    if user_found:
        if user_found['password']==password:
            return render_template('home.html',user = username.capitalize())
        else:
            return render_template('login.html',message="wrong password")
    else:
        return render_template('login.html',message="user not found")

@app.route('/register',methods=['GET','POST'])
def register():
    records = db.user
    username = request.form['uname']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['pass']

    if records.find_one({"name":username}):
        return render_template('login.html',message="username already exists")
    elif records.find_one({"email":email}):
        return render_template('login.html',message="email already exists")
    elif records.find_one({"phone":phone}):
        return render_template('login.html',message="email already exists")
    else:
        user_input = {'username': username, 'email': email, 'phone':phone,'password': password}
        records.insert_one(user_input)
        return render_template('login.html',message="user successfully registered. Please login")

@app.route('/speech_to_image',methods = ['POST','GET'])
def speech_to_image():
    return render_template('voice.html')

@app.route('/word_by_word',methods = ['POST','GET'])
def word_by_word():
    text = request.form['speech']
    everything=process1.part(text)
    ####
    # user = "ashwin"
    # email = "ashwin2001"
    # password = "password"
    # user_input = {'name': user, 'email': email, 'password': password}
    # user_found = records.find_one({"name": user})
    # print(user_found["password"])
    # if user_found:
    #     print("already exists")
    # else:
    #     records.insert_one(user_input)
    #####
    # print(everything[1][1])
    return render_template('display.html',everything=everything,len=len(everything),flag=0)

@app.route('/whole_word',methods = ['POST','GET'])
def whole_word():
    text = request.form['speech']
    everything=process1.part(text.replace(" ",""))
    ####
    # user = "ashwin"
    # email = "ashwin2001"
    # password = "password"
    # user_input = {'name': user, 'email': email, 'password': password}
    # user_found = records.find_one({"name": user})
    # print(user_found["password"])
    # if user_found:
    #     print("already exists")
    # else:
    #     records.insert_one(user_input)
    #####
    # print(everything[1][1])
    everything_word=[]
    for word in everything:
        everything_word.append(tuple((text,word[1],word[2])))
    return render_template('display.html',everything=everything_word,len=len(everything),flag=1)

@app.route('/addprodpage',methods = ['POST','GET'])
def addprodpage():
    return render_template('/admin/addprod.html')

# @app.route('/addprod',methods = ['POST','GET'])
# def addprod():
#     records=db.products
#     prodname=request.form['pname']
#     compname=request.form['cname']
#     price=request.form['price']
#     desc=request.form['description']
#     prodimage=request.form['prodimage']

#     prod_input={'pname':prodname,'cname':compname,'price':price,'description':desc,'image':prodimage}
#     records.insert_one(prod_input)
#     return render_template('/admin/addprod.html')

@app.route('/addprod',methods = ['POST','GET'])
def addprod():
    records=db.products
    prodname=request.form['pname']
    compname=request.form['cname']
    price=request.form['price']
    desc=request.form['description']
    prodimage = request.form['prodimage']
    if 'prodimage' in request.files:
        prodimageName=request.files['prodimage']
        fss = gridfs.GridFS(db)
        fss.put(prodimageName,filename=prodimageName.filename)
        # return render_template('admin.html')

    # prod_input={'pname':prodname,'cname':compname,'price':price,'description':desc,'image':prodimage}
    # records.insert_one(prod_input)
    return render_template('/admin/addprod.html')
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/prodshow',methods = ['POST','GET'])
def prodshow():
    records=db.products
    products=records.find()

    data = db.fs.files.find()
    # my_id = data['_id']
    # outputdata = fs.get(my_id).read()

    return render_template('products.html',products=records.find(),min=products.sort("price", -1).limit(1),max=products.sort("price", 1).limit(1),img=data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)