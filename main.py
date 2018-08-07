import os
from flask import Flask,render_template,request
from resumidor import uplaod_file
from noticias import scrapping_news
from clustering  import startClustering

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/noticias', methods=['GET', 'POST'])
def noticias():
    if request.method == 'POST':
        return scrapping_news()
    else:
        return render_template('noticias.html')

@app.route('/resumidor', methods=['GET', 'POST'])
def resumidor():
    if request.method == 'POST':
        return uplaod_file()
    else:
        return render_template('resumidor.html')

@app.route('/clustering')
def render_clustering():
    return render_template('clustering.html',data = startClustering())

if __name__ == "__main__":
    app.run(debug=True)
