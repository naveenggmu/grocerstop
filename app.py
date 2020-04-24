from flask import *
from functions import *

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')    
@app.route('/addShop', methods=['GET','POST'])
def goto():
    if(request.method=='GET'):
        return render_template('addShop.html')
    else:    
        to = enterShopName(request)
        return render_template('addShop.html', t=to)
        

if __name__ == "__main__":
    app.run(debug=True)
