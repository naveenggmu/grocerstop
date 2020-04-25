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
        db.child("shops").child(name).update({"location" : location, "image": image})
        shops=db.child("shops").get()
        to=shops.val()
        for key,value in to.items():
            print(key,value['location'])
        return to

def locationwise(request):
    if request.method == 'POST':
        location=request.form['location']
    shops=db.child("shops").get()
    locationshops=OrderedDict()

    for key,value in shops.val().items():
        if(value['location']==location):
            locationshops[key]=value
    return locationshops

    return shops

