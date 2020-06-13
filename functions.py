# db.child("names").push({"name":"kevin"})
# db.child("names").child("name").update({"name":"naveen"})
# users=db.child("names").child("name").get()
# print(users.val())
# print(users.key())
import pyrebase
import pyqrcode
from datetime import datetime

from collections import OrderedDict

config={
    "apiKey" : "AIzaSyDYowAfpHnLS5xqujO-hZyrQg2M4IkvJQk",
    "authDomain" : "grocerstop-6ff7b.firebaseapp.com",
    "databaseURL" : "https://grocerstop-6ff7b.firebaseio.com",
    "projectId" : "grocerstop-6ff7b",
    "storageBucket" : "grocerstop-6ff7b.appspot.com",
    "messagingSenderId" : "411449174332",
    "appId" : "1:411449174332:web:19c4eb6040dc76a9b5d639",
    "measurementId" : "G-B4JTE77M3V"
}

firebase = pyrebase.initialize_app(config)
auth= firebase.auth()

db= firebase.database()
# from flask import render_template
def enterShopDetails(request):
    if request.method == 'POST':
        name=request.form['name']
        location=request.form['location']
        image=request.form['image']
        userid=request.form['id']
        shops=db.child("shops").get()
        db.child("shops").update({userid:{"name" : name ,"location" : location, "image": image, "people": 0}})
        to=shops.val()
        return to

def locationwise(request):
    if request.method == 'POST':
        location=request.form['location']
    shops=db.child("shops").get().val()
    locationshops=OrderedDict()


    for key,value in shops.items():
        if(value['location']==location):
            locationshops[key]=value
    return locationshops

    return shops

def countchange(request):
    userid=request.form['userid']
    countinc=(request.form['countinc'])
    countdec=(request.form['countdec'])
    if(countinc==""):
        countinc=0
    if(countdec==""):
        countdec=0
    details=db.child("shops").child(userid).get().val()
    count=int(details['people'])
    print(type(count),count, type(countinc),countinc, type(countdec),countdec)
    count=count + int(countinc) - int(countdec)
    if(count<0):
        count=0
    db.child("shops").child(userid).update({"people":count})

def addProducts(request):
    userid = request.form['userid']
    fruits = request.form.get('fruits')
    veg = request.form.get('vegetables')
    diary = request.form.get('diary')
    if(fruits==None):
        fruits='off'
    if(veg==None):
        veg = 'off'
    if(diary==None):
        diary='off'            
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    db.child("products").update({userid : {'diary': diary,'vegetables': veg,'fruits': fruits,'lastUpdated': dt_string }})
    data = db.child('products').get().val()
    return data

def authentication(request):
    email=request.form['email']
    password=request.form['password']
    try:
        user=auth.sign_in_with_email_and_password(email,password)
        return user
    except:
        return 0 
    
def register(request):
    try:
        email=request.form['email']
        password=request.form['password']
        auth.create_user_with_email_and_password(email,password)
    except:
        print("allready registered")


def custShopBookingDisplay(shopid):
    data_products = db.child('products').child(shopid).get().val()
    data_shop = db.child('shops').child(shopid).get().val()
    return data_products,data_shop

#LOGIC FOR ADDING SLOT BOOKING WRT TO THE CURRENT TIME SHOULD BE WRITTEN
#IN bookingstatus()
def bookingstatus(request):
    
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    print(date)
    print(request.form['custid'])
    print(request.form['slotOption'])

def flutterShopVerify(request):

    print("request method")
    print(request.method)
    x  = request.get_json(force = True)
    print("Contents in x")
    print(x)
    if(x):
        shop_id = x['shop_id']
        passwd = x['password']

        actual_pwd = db.child('shops').child(shop_id).child("shopPassword").get().val()
        print("Shop id ",shop_id)
        print("passwd ",passwd)
        
        print("Actual pwd ",actual_pwd)
        if(str(actual_pwd) == str(passwd)):
            return db.child('shops').child(shop_id).get().val()
        else:
            return "not in db"
    else:
        return "Wrong data"        


def QRCodeGenerator(content_qr):
    url = pyqrcode.create(content_qr)
    url.svg('/huca-url.svg', scale=8)
    
