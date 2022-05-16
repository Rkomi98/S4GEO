# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:55:16 2022

@author: mirko
"""
from flask import (Flask,
                   render_template,
                   request,
                   session, 
                   redirect, 
                   url_for)
from psycopg2 import ( 
    connect
) 
app = Flask(__name__,template_folder="templates")

@app.route('/') 
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    conn = connect("dbname=S4G user=postgres password=Gram2021")
    cur = conn.cursor() 
    cur.execute( """SELECT blog_user.user_name,
                post.title, 
                post.body FROM blog_user,
                post WHERE blog_user.user_id = post.author_id""" )
    posts = cur.fetchall() 
    print(posts) 
    cur.close()
    conn.commit()
    return render_template('index.html', title='Home', user=user, posts=posts)
# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)