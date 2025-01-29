from flask import Flask, render_template
from flask import request
import time

app = Flask(__name__)

@app.route('/')
def hello_world():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    baseurl = request.base_url
    return render_template('index.html', ip=ip, baseurl=baseurl, headers=request.headers)

@app.route('/contents/index.html')
def contents():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    baseurl = request.base_url
    return render_template('contents.html', ip=ip, baseurl=baseurl, headers=request.headers)

@app.route('/size/')
def size():
    if request.args.get('v') is None:
        return render_template('size.html', size=1)
    elif request.args.get('size').isnumeric() is False:
        return render_template('size.html', size=1)
    else: 
        return render_template('size.html', size=int(request.args.get('v')))
    
@app.route('/sleep/')   
def sleep():
    if request.args.get('v') is None:
        time.sleep(1)
        return render_template('sleep.html', time=1)
    elif request.args.get('v').isnumeric() is False:
        time.sleep(1)
        return render_template('sleep.html', time=1)
    else: 
        time.sleep(int(request.args.get('v')))
        return render_template('sleep.html', time=int(request.args.get('v'))), 499
    
@app.route('/health/')   
def health():
    time.sleep(30)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, port=4996)
