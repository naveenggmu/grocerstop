# db.child("names").push({"name":"kevin"})
# db.child("names").child("name").update({"name":"naveen"})
# users=db.child("names").child("name").get()
# print(users.val())
# print(users.key())
import pyrebase
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


