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
from os import name
import re
from dns.message import Message
from flask import Flask,jsonify,request
from flask import render_template
from flask.json import jsonify
from nltk.util import pr
# from pymongo import message
# from flask import flask_pymongo as fp
# from fp import PyMongo
import gridfs
import process1
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.aq5jb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('mongodata')
# mongo = pymongo.PyMongo(app)
# mongo = fp.PyMongo(app)
# fs = gridfs.GridFS(mongo.db)

# @app.route('/',methods = ['GET', 'POST'])
# def home():  # put application's code here
#     return render_template("voice.html")

@app.route('/',methods = ['GET', 'POST'])
def index():  # put application's code here
    return render_template("login1.html")

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
            return render_template('login1.html',message="wrong password")
    else:
        return render_template('login1.html',message="user not found")

@app.route('/register',methods=['GET','POST'])
def register():
    records = db.user
    username = request.form['uname']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['pass']

    if records.find_one({"name":username}):
        return render_template('login1.html',message="username already exists")
    elif records.find_one({"email":email}):
        return render_template('login1.html',message="email already exists")
    elif records.find_one({"phone":phone}):
        return render_template('login1.html',message="email already exists")
    else:
        user_input = {'username': username, 'email': email, 'phone':phone,'password': password}
        records.insert_one(user_input)
        return render_template('login1.html',message="user successfully registered. Please login")

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
    return render_template('display.html',everything=everything,len=len(everything),flag=0,text=text)

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
    return render_template('display.html',everything=everything_word,len=len(everything),flag=1,text=text)

@app.route('/addprodpage',methods = ['POST','GET'])
def addprodpage():
    return render_template('/admin/addprod.html')

@app.route('/addprod',methods = ['POST','GET'])
def addprod():
    records=db.products
    prodname=request.form['pname']
    compname=request.form['cname']
    price=request.form['price']
    desc=request.form['description']
    pimage=request.form['prodimage']

    prod_input={'pname':prodname,'cname':compname,'price':price,'description':desc,'image':pimage}
    records.insert_one(prod_input)
    return render_template('/admin/addprod.html')

# @app.route('/addprod',methods = ['POST','GET'])
# def addprod():
#     records=db.products
#     prodname=request.form['pname']
#     compname=request.form['cname']
#     price=request.form['price']
#     desc=request.form['description']
#     # prodimage = request.form['prodimage']
#     # if 'prodimage' in request.files:
#     #     prodimageName=request.files['prodimage']
#     #     fss = gridfs.GridFS(db)
#     #     fss.put(prodimageName,filename=prodimageName.filename)
#     #     # return render_template('admin.html')

#     prod_input={'pname':prodname,'cname':compname,'price':price,'description':desc,'image':prodimage}
#     records.insert_one(prod_input)
#     return render_template('/admin/addprod.html')

# @app.route('/file/<filename>')
# def file(filename):
#     return mongo.send_file(filename)

@app.route('/prodshow',methods = ['POST','GET'])
def prodshow():
    records=db.products
    products=records.find()
    products1=records.find()

    records2=db.cart
    val = records2.count_documents({})

    data = db.fs.files.find()
    # my_id = data['_id']
    # outputdata = fs.get(my_id).read()
    minprod=products.sort("price", 1).limit(1);
    maxprod=products1.sort("price", -1).limit(1);
    for minp in minprod:
        min=minp['price']
    for maxp in maxprod:
        max=maxp['price']
    print(min)
    return render_template('products.html',products=records.find(),min=min,max=max,filter=records.find(),val=val)

@app.route('/to_admin',methods = ['POST','GET'])
def to_admin():
    return render_template('/admin/admin.html')

@app.route('/inventory_check',methods = ['POST','GET'])
def inventory_check():
    records=db.products
    return render_template('/admin/inventory.html',products=records.find())

@app.route('/users_check',methods = ['POST','GET'])
def users_check():
    records=db.user
    users=records.find()
    # for user in users:
    #     print(user['username'])
    return render_template('/admin/adminusers.html',users=users)


@app.route('/delete_prod',methods = ['POST','GET'])
def delete_prod():
    records=db.products
    prodname=request.form['delete_id']
    myQuery ={'pname':prodname}
    records.delete_one(myQuery)
    return render_template('/admin/inventory.html',products=records.find())

@app.route('/to_edit_prod',methods = ['POST','GET'])
def to_edit_prod():
    edit_id=request.form['edit_id']
    records=db.products
    prod=records.find_one({"pname":edit_id})
    # for prod in products:
    #     print(type(prod))
    # print(type(products))
    return render_template('/admin/editprod.html',edit=edit_id,prod=prod)

@app.route('/edit_prod',methods = ['POST','GET'])
def edit_prod():
    records=db.products
    prodname_edit=request.form['edit_id']
    prodname=request.form['pname']
    compname=request.form['cname']
    price=request.form['price']
    desc=request.form['description']

    records.find_one_and_update({'pname':prodname_edit},
                                {'$set':{'pname':prodname,'cname':compname,'price':price,'description':desc}})

    return render_template('/admin/inventory.html',products=records.find())

@app.route('/admin',methods=['GET','POST'])
def admin():
    records = db.admin
    username=request.form['auname']
    password=request.form['apass']
    
    user_found = records.find_one({"username": username})
    if user_found:
        if user_found['password']==password:
            return render_template('/admin/admin.html')
        else:
            return render_template('login1.html',message="wrong admin credentials")
    else:
        return render_template('login1.html',message="wrong admin credentials")

@app.route('/pricefilter',methods = ['POST','GET'])
def pricefilter():
    records=db.products
    products=records.find()
    products1=records.find()

    mina=request.form['min']
    maxa=request.form['max']

    query = records.find({'price': { '$gt': mina, '$lt': maxa}})

    minprod=products.sort("price", 1).limit(1);
    maxprod=products1.sort("price", -1).limit(1);
    for minp in minprod:
        min=minp['price']
    for maxp in maxprod:
        max=maxp['price']

    return render_template('products.html',products=query,min=min,max=max,filter=records.find())

    # return render_template('products.html')

@app.route('/brand',methods = ['POST','GET'])
def brand():
    print("in")
    records=db.products
    products=records.find()
    products1=records.find()

    com=request.form['brand']

    query = records.find({'cname': com})

    minprod=products.sort("price", 1).limit(1);
    maxprod=products1.sort("price", -1).limit(1);
    for minp in minprod:
        min=minp['price']
    for maxp in maxprod:
        max=maxp['price']

    return render_template('products.html',products=query,min=min,max=max,filter=records.find())

@app.route('/addcart',methods = ['POST','GET'])
def addcart():
    records1=db.cart
    prodname=request.form['cpname']
    compname=request.form['ccname']
    price=request.form['cprice']
    desc=request.form['cdescription']
    pimage=request.form['cimage']

    prod_input={'pname':prodname,'cname':compname,'price':price,'description':desc,'image':pimage}
    records1.insert_one(prod_input)

    records=db.products
    products=records.find()
    products1=records.find()

    records2=db.cart
    val = records2.count_documents({})

    data = db.fs.files.find()
    # my_id = data['_id']
    # outputdata = fs.get(my_id).read()
    minprod=products.sort("price", 1).limit(1);
    maxprod=products1.sort("price", -1).limit(1);
    for minp in minprod:
        min=minp['price']
    for maxp in maxprod:
        max=maxp['price']

    return render_template('products.html',products=records.find(),min=min,max=max,filter=records.find(),val=val)

@app.route('/to_cart',methods = ['POST','GET'])
def to_cart():
    records=db.cart
    totalcost=0
    cartprods = records.find()
    for cprod in cartprods:
        totalcost+=int(cprod['price'])
    return render_template('cart.html',products=records.find(),totalcost=totalcost)

@app.route('/delete_cart',methods = ['POST','GET'])
def delete_cart():
    records=db.cart
    prodname=request.form['delete_id']
    myQuery ={'pname':prodname}
    records.delete_one(myQuery)
    totalcost=0
    cartprods = records.find()
    for cprod in cartprods:
        totalcost+=int(cprod['price'])
    return render_template('cart.html',products=records.find(),totalcost=totalcost)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)