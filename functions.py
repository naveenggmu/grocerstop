# db.child("names").push({"name":"kevin"})
# db.child("names").child("name").update({"name":"naveen"})
# users=db.child("names").child("name").get()
# print(users.val())
# print(users.key())
import pyrebase
import pyqrcode
import png
import smtplib
import imghdr
from email.message import EmailMessage
from datetime import datetime
import datetime as das

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
        people=request.form['capacity']
        shops=db.child("shops").get()
        db.child("shops").update({userid:{"name" : name ,"location" : location, "image": image, "people": people}})
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

def printingAvailableSlots(shopid):

    cap = db.child('realTimeCount').child(shopid).child("CapacityPerSlot").get().val()
    currentDay = db.child('realTimeCount').child(shopid).child("currentDay").get().val()
    nextDay = db.child('realTimeCount').child(shopid).child("nextDay").get().val()
    available_currentDay =OrderedDict()
    now = datetime.now()
    dt_string = now.strftime("%H:%M")
    hours,mins = dt_string.split(':')
    new_time = int(hours + mins)
    for i,j in currentDay.items():
        if(new_time<int(j['startTime'])):
            j['startTime'] = str(j['startTime'])
            available_currentDay[i] = j
        #     if(j['currentCapacity']<cap):
        #         j['startTime'] = str(j['startTime'])
        #         # j['endTime'] = str(j['endTime'])
        #         available_currentDay[i] = j

    available_nextDay =OrderedDict()
    for i,j in nextDay.items():
        j['startTime'] = str(j['startTime'])
        available_nextDay[i] = j
        # if(j['currentCapacity']<cap):
        #     j['startTime'] = str(j['startTime'])
        #     # j['endTime'] = str(j['endTime'])
        #     available_nextDay[i] = j 

    data_shop = db.child('shops').child(shopid).get().val()
    return available_currentDay,available_nextDay,data_shop,cap



def confirmBooking(request,shopid):

    what_day = 0
    print("Going to function")
    slot_id = request.form.get("slotOption")
    cust_id = request.form.get("custid")
    
    booking_id = "_" + slot_id +  "_" + cust_id + "_"
    
    #Increment in realTimeCount
    curr_count = db.child('realTimeCount').child(shopid).child("currentDay").child(slot_id).child('currentCapacity').get().val()
    print(curr_count)
    curr_count+=1

    db.child('realTimeCount').child(shopid).child("currentDay").child(slot_id).update({'currentCapacity' : curr_count})

    db.child('bookings').child(shopid).child("currentDay").child(slot_id).update({booking_id : 0})
    timing = db.child('realTimeCount').child(shopid).child("currentDay").child(slot_id).child("startTime").get().val()

    QRCodeGenerator(booking_id)
    mailGenerator(cust_id,shopid,what_day,timing)

def confirmBooking2(request,shopid):
    
    what_day = 1
    print("Going to function")
    slot_id = request.form.get("slotOption")
    cust_id = request.form.get("custid")
    
    booking_id = "_" + slot_id +  "_" + cust_id + "_"
    
    #Increment in realTimeCount
    curr_count = db.child('realTimeCount').child(shopid).child("nextDay").child(slot_id).child('currentCapacity').get().val()
    print(curr_count)
    curr_count+=1

    db.child('realTimeCount').child(shopid).child("nextDay").child(slot_id).update({'currentCapacity' : curr_count})

    db.child('bookings').child(shopid).child("nextDay").child(slot_id).update({booking_id : 0})
    timing = db.child('realTimeCount').child(shopid).child("nextDay").child(slot_id).child("startTime").get().val()
    QRCodeGenerator(booking_id)
    mailGenerator(cust_id,shopid,what_day,timing)   



def flutterUserVerify(request):

    jso = request.get_json(force = True)
    key = jso['val']
    shopid = jso['shop_id']
    slot_id = key.split('_')[1]
    x = db.child('bookings').child(shopid).child("currentDay").child(slot_id).child(key).get().val()
    data = {}
    if(x==None):
        data['status'] = False
        data['info'] = "Invalid Booking"
    else:
        if(x==0):
            data['status'] = True
            data['info'] = "user verified"
            db.child('bookings').child(shopid).child("currentDay").child(slot_id).update({booking_id : 1})
        else:
            data['status'] = False
            data['info'] = "user already entered"
    return data     











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
        data = {}
        if(str(actual_pwd) == str(passwd)):
            data['details'] = db.child('shops').child(shop_id).get().val()
            
            data['status'] = True
            return data
        else:
            data['status'] = False
            return data
    else:
        return "Wrong data"      





def QRCodeGenerator(content_qr):
    url = pyqrcode.create(content_qr)
    url.png('barcode.png',scale = 8)
    

def mailGenerator(cust_id,shopid,what_day,timing):
    
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    if(what_day == 1):
        
        today=das.datetime.today()
        month=today.month
        year=today.year
        day=today.day + 1
        date = das.date(year, month, day).strftime('%d-%m-%Y') 

    mail_id = db.child("customers").child(cust_id).child('email').get().val()

    
    
    msg = EmailMessage()
    
    msg['Subject'] = "grocerstop Booking Barcode"
    msg['From'] = "cudamemerror@gmail.com"

    msg['To'] = mail_id
    contents = "Booking confirmed for " + shopid + " on " + date + " at " + str(timing)
    msg.set_content(contents)

    with open('barcode.png','rb') as f:
        file_data =f.read()
        file_type = imghdr.what(f.name)
        file_name = "Barcode"

    msg.add_attachment(file_data,maintype='image',subtype='png')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("cudamemerror@gmail.com", "ImageClef1@")
        smtp.send_message(msg)