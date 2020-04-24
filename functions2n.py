import pyrebase

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
def enterShopName(request):
    if request.method == 'POST':
        name=request.form['name']
        db.child("shops").push(name)
        todo=db.child("shops").get()
        to=todo.val()
        return to