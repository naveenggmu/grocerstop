from flask import Flask, redirect, url_for, request 
app = Flask(__name__) 
  
@app.route('/')
def mainpage():
    return "Hello World . THis is naveen"  
@app.route('/success/<name>') 
def success(name):
    str = "welcome "+name
    return str 
  
@app.route('/login/',methods = ['POST']) 
def login(): 
    # x = request.form
    print(request.args)
    print(request.files)
    print(request.form)
    x= request.form
    print("request form {}".format(x['check']))
    # print("name {}".format(x['name']))
    return "Check server"
  
if __name__ == '__main__': 
   app.run(debug = True) 
