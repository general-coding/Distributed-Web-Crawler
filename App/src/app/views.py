'''
Created on Apr 29, 2015

@author: puneeth
'''

from app import app
from flask.templating import render_template 
from flask import request, redirect, url_for
from crawler.Crawl_Master import init

@app.route('/')
@app.route('/index')
def index():
#     return "Hello, World!"
    user = {'nickname':'Puneeth',
            'friend': 'Nishanth'}  # fake user
      
    return render_template('index.html',
                           title='Distributed Web Crawler',
                           user=user)

@app.route('/crawl', methods=['POST'])
def crawl():
    url = request.form['url']
#     print("We will crawl : " + url)
    
    init(url)
    return redirect(url_for('display'))

@app.route('/display')
def display():
    print("Urls below:")
    
    f= open('input.txt','r')
    j=[]
    for line in f:
        j.append(line)
    
    return render_template('display.html',obj=j)
