#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request
app = Flask(__name__, static_url_path='/static')


data = [0,1,2,3,4,5,6,7,8,9]


@app.route('/')
def index():
    return app.send_static_file('raindance.html')

@app.route('/json')
def json():
    return str(data)

@app.route('/put', methods=['GET','POST'])
def put():
    global data
    data = request.get_json()
    print data
    return '400'

if __name__ == '__main__':
    app.run(debug=True)