from flask import *
from functions import *

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    to = enterShopName(request)
    return render_template('index.html', t=to)

if __name__ == "__main__":
    app.run(debug=True)
