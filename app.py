from flask import *
from functions import *
from collections import OrderedDict

app=Flask(__name__)
@app.route('/', methods=['GET','POST'])
def mainpage():
    return render_template('mainpage.html')

@app.route('/customerlogin', methods=['GET','POST'])
def customerlogin():
    if request.method=="GET":
        return render_template("Customer/customerlogin.html")
    else:
        user = authentication(request)
        if(user==0):
            print("no user")
            return render_template("Customer/customerlogin.html")
        else:
            print(user)
            return render_template('index.html') 
        
@app.route('/customerregister', methods=['GET','POST'])
def customerregister():
    if request.method=="GET":
        return render_template("Customer/customerregister.html")
    else:
        register(request)
        print("registered")
        return redirect(url_for('customerlogin'))

@app.route('/test', methods=['GET','POST'])
def index():
    return render_template('index.html')  
  
@app.route('/addShop', methods=['GET','POST'])
def goto():
    if(request.method=='GET'):
        shops=db.child("shops").get().val()
        print(shops)
        for key,values in shops.items():
            print(key,values)

        return render_template('Shopkeeper/addShop.html',t=shops)

    else:    
        to = enterShopDetails(request)
        return render_template('Shopkeeper/addShop.html', t=to)

@app.route('/customerPage', methods=['GET','POST'])
def goto1():
    if(request.method=='GET'):
        shops=db.child("shops").get().val()
        print(shops)
        return render_template('Customer/customerPage.html',t=shops)
    else:
        shops=locationwise(request)
        print(shops)
        return render_template('Customer/customerPage.html',t=shops)        

@app.route('/addcustomer', methods=['GET','POST'])
def addcustomers():
    if(request.method=='GET'):
        return render_template('Shopkeeper/addcustomer.html')
    else:
        countchange(request)
        return render_template('Shopkeeper/addcustomer.html')

@app.route('/addProducts', methods=['GET','POST'])
def addProd():
    if(request.method=='GET'):
        return render_template('Shopkeeper/addProducts.html')
    else:
        data = addProducts(request)
        return render_template('Shopkeeper/addProducts.html', data = data)            

@app.route('/customerBookingShop/<shopid>',methods=['GET','POST'])
def custbook(shopid):
    if(request.method=='GET'):
        currDay,nextDay,data_shop = printingAvailableSlots(shopid)
        data = {
            'currentDay' : currDay,
            'nextDay' : nextDay,
            'data_shop' : data_shop

        }
        return render_template('Customer/customerBookingShop.html',data = data)

# def custBook(shopid):
#     print("Inside custBook")
#     if(request.method=='GET'):   
#         x,y = custShopBookingDisplay(shopid)
#         data = {'shop_data': y,
#                 'shop_products' : x,
#                 'shopid': shopid,
#                 'bookingStatus': ""}
#         return render_template('Customer/customerBookingShop.html',data = data)
#     elif(request.method=='POST'):
#         print("Into elif")
#         bookingstatus(request)
#         x,y = custShopBookingDisplay(shopid)
#         data = {'shop_data': y,
#                 'shop_products' : x,
#                 'shopid': shopid,
#                 'bookingStatus': "Updated"}
#         return render_template('Customer/customerBookingShop.html',data = data)    









######################################################### FOR FLUTTER ####################################################

@app.route('/flutterShopVerify',methods=['POST'])
def func():
    info = flutterShopVerify(request)
    return info









if __name__ == "__main__":
    app.run(debug=True)
