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
        shops=db.child("shops").get()
        db.child("shops").push({name : {"location" : location, "image": image}})
        to=shops.val()
        return to

def locationwise(request):
    if request.method == 'POST':
        location=request.form['location']
    shops=db.child("shops").get().val()
    locationshops=OrderedDict()

    for i,j in shops.items():
        for key,value in j.items():
            if(value['location']==location):
                locationshops[key]=j
    return locationshops

    return shops

