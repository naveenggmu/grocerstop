from flask import *
from functions import *
from collections import OrderedDict

app=Flask(__name__)
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')  
  
@app.route('/addShop', methods=['GET','POST'])
def goto():
    if(request.method=='GET'):
        shops=db.child("shops").get().val()
        print(shops)
        for key,values in shops.items():
            print(key,values)

        return render_template('addShop.html',t=shops)

    else:    
        to = enterShopDetails(request)
        return render_template('addShop.html', t=to)

@app.route('/customerPage', methods=['GET','POST'])
def goto1():
    if(request.method=='GET'):
        shops=db.child("shops").get().val()
        print(shops)
        return render_template('customerPage.html',t=shops)
    else:
        shops=locationwise(request)
        print(shops)
        return render_template('customerPage.html',t=shops)        

@app.route('/addcustomer', methods=['GET','POST'])
def addcustomers():
    if(request.method=='GET'):
        return render_template('addcustomer.html')
    else:
        countchange(request)
        return render_template('addcustomer.html')

@app.route('/addProducts', methods=['GET','POST'])
def addProd():
    if(request.method=='GET'):
        return render_template('addProducts.html')
    else:
        data = addProducts(request)
        return render_template('addProducts.html', data = data)            

if __name__ == "__main__":
    app.run(debug=True)
