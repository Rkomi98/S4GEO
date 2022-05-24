#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 06:43:11 2019

@author: Mirko
"""

from flask import (
    Flask, render_template, request, redirect, flash, url_for, session, g
)

from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.exceptions import abort

from psycopg2 import (
    connect
)
import requests
import json
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))

# Create the application instance
app = Flask(__name__, template_folder="templates")
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def get_dbConn():
    if 'dbConn' not in g:
        myFile = open('dbConfig.txt')
        connStr = myFile.readline()
        g.dbConn = connect(connStr)

    return g.dbConn


def close_dbConn():
    if 'dbConn' in g:
        g.dbComm.close()
        g.pop('dbConn')


def get_json_API(city):
    link = "https://api.waqi.info/feed/" + city + \
        "/?token=6b937a38a89b944787d29b8afca33fe1cf375bd1"
    response = requests.get(link)

    if str(response) != "<Response [200]>":
        txt = "Invalid city name. No data found for: " + city
        raise Exception(txt)

    raw_data = response.text
    data = json.loads(raw_data)
    return data


def get_forecast_data(city):
    data = get_json_API(city)

    # from JSON to Pandas DataFrame: creating the forecast table

    # extracting all the factors seperately:
    data_df_forecast_o3 = pd.json_normalize(
        data['data']['forecast']['daily']['o3'])
    data_df_forecast_pm10 = pd.json_normalize(
        data['data']['forecast']['daily']['pm10'])
    data_df_forecast_pm25 = pd.json_normalize(
        data['data']['forecast']['daily']['pm25'])
    data_df_forecast_uvi = pd.json_normalize(
        data['data']['forecast']['daily']['uvi'])

    # preparing each of them to be merged later:
    data_df_forecast_o3 = data_df_forecast_o3.rename(
        columns={'avg': 'avg_o3', 'max': 'max_o3', 'min': 'min_o3'})
    data_df_forecast_o3.insert(0, 'day', data_df_forecast_o3.pop('day'))

    data_df_forecast_pm10 = data_df_forecast_pm10.rename(
        columns={'avg': 'avg_pm10', 'max': 'max_pm10', 'min': 'min_pm10'})
    data_df_forecast_pm10.insert(0, 'day', data_df_forecast_pm10.pop('day'))

    data_df_forecast_pm25 = data_df_forecast_pm25.rename(
        columns={'avg': 'avg_pm25', 'max': 'max_pm25', 'min': 'min_pm25'})
    data_df_forecast_pm25.insert(0, 'day', data_df_forecast_pm25.pop('day'))

    data_df_forecast_uvi = data_df_forecast_uvi.rename(
        columns={'avg': 'avg_uvi', 'max': 'max_uvi', 'min': 'min_uvi'})
    data_df_forecast_uvi.insert(0, 'day', data_df_forecast_uvi.pop('day'))

    # merging all the factors in one prediction table:
    o3_pm10 = pd.merge(data_df_forecast_o3,
                       data_df_forecast_pm10, how="outer", on=["day"])
    o3_pm10_pm25 = pd.merge(
        o3_pm10, data_df_forecast_pm25, how="outer", on=["day"])
    final_forecast_table = pd.merge(
        o3_pm10_pm25, data_df_forecast_uvi, how="outer", on=["day"])

    final_forecast_table_html = final_forecast_table.to_html()

    return final_forecast_table_html


def get_realtime_data(city):
    data = get_json_API(city)

    # from JSON to Pandas DataFrame: creating the real time data table
    data_df_day = pd.json_normalize(data['data'])

    # dropping the unnecessary columns:
    data_df_day = data_df_day.drop(columns=['idx', 'attributions', 'dominentpol', 'city.url', 'city.location', 'time.v', 'time.iso',
                                            'forecast.daily.o3', 'forecast.daily.pm10', 'forecast.daily.pm25', 'forecast.daily.uvi', 'debug.sync'])

    # renaming the columns we will be using for clarity:
    data_df_day = data_df_day.rename(columns={'city.name': 'city', 'aqi': 'air quality','iaqi.co.v': 'carbon monoxyde',
                                              'iaqi.h.v': 'relative humidity', 'iaqi.no2.v': 'nitrogen dioxide',
                                              'iaqi.o3.v': 'ozone', 'iaqi.p.v': 'atmospheric pressure', 'iaqi.pm10.v': 'PM10',
                                              'iaqi.pm25.v': 'PM2.5', 'iaqi.so2.v': 'sulphur dioxide', 'iaqi.t.v': 'temperature',
                                              'iaqi.w.v': 'wind', 'time.s': 'date and time', 'time.tz': 'time zone'})

    # creating two columns for geographical coordinates instead of one for easier access:
    data_df_day['lat'] = data_df_day['city.geo'][0][0]
    data_df_day['lon'] = data_df_day['city.geo'][0][1]
    data_df_day = data_df_day.drop(columns=['city.geo'])

    final_realtime_table = gpd.GeoDataFrame(
        data_df_day, geometry=gpd.points_from_xy(data_df_day['lon'], data_df_day['lat']))

    final_realtime_table_html = final_realtime_table.to_html()

    return final_realtime_table_html

def get_data_toDB(city):
    data = get_json_API(city)

    # from JSON to Pandas DataFrame: creating the real time data table
    data_df_day = pd.json_normalize(data['data'])

    # dropping the unnecessary columns:
    data_df_day = data_df_day.drop(columns=['idx', 'attributions', 'dominentpol', 'city.url', 'city.location', 'time.v', 'time.iso',
                                            'forecast.daily.o3', 'forecast.daily.pm10', 'forecast.daily.pm25', 'forecast.daily.uvi', 'debug.sync'])

    # renaming the columns we will be using for clarity:
    data_df_day = data_df_day.rename(columns={'city.name': 'city',
                                              'aqi': 'air_quality',
                                              'iaqi.co.v': 'carbon_monoxyde',
                                              'iaqi.h.v': 'relative_humidity',
                                              'iaqi.no2.v': 'nitrogen_dioxide',
                                              'iaqi.o3.v': 'ozone', 
                                              'iaqi.p.v': 'atmospheric_pressure', 
                                              'iaqi.pm10.v': 'PM10',
                                              'iaqi.pm25.v': 'PM25', 
                                              'iaqi.so2.v': 'sulphur_dioxide',
                                              'iaqi.t.v': 'temperature',
                                              'iaqi.w.v': 'wind', 
                                              'time.s': 'date_and_time', 
                                              'time.tz': 'time zone'
                                              })

    # creating two columns for geographical coordinates instead of one for easier access:
    data_df_day['lat'] = data_df_day['city.geo'][0][0]
    data_df_day['lon'] = data_df_day['city.geo'][0][1]
    data_df_day = data_df_day.drop(columns=['city.geo'])
    data_df_day = data_df_day.drop('time zone', 1)
    final_realtime_table = gpd.GeoDataFrame(
        data_df_day, geometry=gpd.points_from_xy(data_df_day['lon'], data_df_day['lat']))
    return final_realtime_table

def sendDFtoDB(db):
    engine = create_engine('postgresql://postgres:Gram2021@localhost:5432/S4G') 
    db.to_postgis('cities', engine, if_exists = 'replace', index=False) #I can put some queries here


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'SELECT user_id FROM blog_user WHERE user_name = %s', (username,))
            if cur.fetchone() is not None:
                error = 'User {} is already registered.'.format(username)
                cur.close()

        if error is None:
            conn = get_dbConn()
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO blog_user (user_name, user_password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            cur.close()
            conn.commit()
            return redirect(url_for('login'))
        else:
            error = "Please register"

        flash(error)

    return render_template('auth/register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_dbConn()
        cur = conn.cursor()
        error = None
        cur.execute(
            'SELECT * FROM blog_user WHERE user_name = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.commit()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        conn = get_dbConn()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM blog_user WHERE user_id = %s', (user_id,)
        )
        g.user = cur.fetchone()
        cur.close()
        conn.commit()
    if g.user is None:
        return False
    else:
        return True


# Create a URL route in our application for "/"
@app.route('/')
@app.route('/index')
def index():
    conn = get_dbConn()
    cur = conn.cursor()
    cur.execute(
        """SELECT blog_user.user_name, post.post_id, post.created, post.title, post.body 
               FROM blog_user, post WHERE  
                    blog_user.user_id = post.author_id"""
    )
    posts = cur.fetchall()
    cur.close()
    conn.commit()
    load_logged_in_user()

    return render_template('index.html', posts=posts)


@app.route('/generic')
def generic():
    conn = get_dbConn()
    cur = conn.cursor()
    cur.execute(
        """SELECT blog_user.user_name, post.post_id, post.created, post.title, post.body 
               FROM blog_user, post WHERE  
                    blog_user.user_id = post.author_id"""
    )
    posts = cur.fetchall()
    cur.close()
    conn.commit()
    load_logged_in_user()

    return render_template('generic.html', posts=posts)


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/createProject', methods=['GET', 'POST'])
def createProject():
    if load_logged_in_user():        
        if request.method == 'POST':
            template = env.get_template("templates/createProject.html")
    
            if request.form['dtype'] == 'F':
                template_vars = {"table1": get_forecast_data(request.form['city']),
                                 "table2": ""}
                html_out = template.render(template_vars)
    
            elif request.form['dtype'] == 'RT':
                template_vars = {"table1": get_realtime_data(request.form['city']),
                                 "table2": ""}
                
                C = get_data_toDB(request.form['city'])                
                """
                conn = get_dbConn()
                cur = conn.cursor()
                time = pd.to_datetime(C.date_and_time)
                cur.execute('INSERT INTO city (author_id, name_city, air_quality, carbon_monoxyde, relative_humidity, nitrogen_dioxide, ozone,atmospheric_pressure,pm10,pm25,so2,temperature,wind,time_zone,latitude,longitude,geometry) VALUES(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                            (g.user[0],
                             C.city[0],
                             float(C.air_quality[0]),
                             C.carbon_monoxyde[0], 
                             C.relative_humidity[0],
                             C.nitrogen_dioxide[0],
                             C.ozone[0], 
                             C.atmospheric_pressure[0],
                             float(C.PM10[0]),
                             float(C.PM25[0]),
                             C.sulphur_dioxide[0],
                             C.temperature[0],
                             float(C.wind[0]),
                             str(time[0]),
                             C.lat[0],
                             C.lon[0],
                             C.geometry)
                            )
                #df.to_sql('bike', engine, if_exists = 'replace', index=False) #I can put some queries here
                cur.close()
                conn.commit()
                
                #return redirect(url_for('index'))
                """
                sendDFtoDB(C)
                html_out = template.render(template_vars)
    
            elif request.form['dtype'] == 'B':
                template_vars = {"table1": get_realtime_data(request.form['city']),
                                 "table2": get_forecast_data(request.form['city'])}
                html_out = template.render(template_vars)
    
            else:
                template_vars = {"table1": '\nInvalid data type! Inputs can be: "F", "RT" or "B"!',
                                 "table2": ""}
                html_out = template.render(template_vars)
    
            return html_out
            # return render_template('createProject.html', tables=get_data(request.form['query']))
    
        return render_template('createProject.html')
    else :
        error = 'Only loggedin users can insert posts!'
        flash(error)
        return redirect(url_for('login'))


"""
@app.route('/create', methods=('GET', 'POST'))
def create():
    if load_logged_in_user():
        if request.method == 'POST' :
            title = request.form['title']
            body = request.form['body']
            error = None
            
            if not title :
                error = 'Title is required!'
            if error is not None :
                flash(error)
                return redirect(url_for('index'))
            else : 
                conn = get_dbConn()
                cur = conn.cursor()
                cur.execute('INSERT INTO post (title, body, author_id) VALUES (%s, %s, %s)', 
                            (title, body, g.user[0])
                            )
                cur.close()
                conn.commit()
                return redirect(url_for('index'))
        else :
            return render_template('blog/index.html')
    else :
        error = 'Only loggedin users can insert posts!'
        flash(error)
        return redirect(url_for('login'))
 """


def get_post(id):
    conn = get_dbConn()
    cur = conn.cursor()
    cur.execute(
        """SELECT *
           FROM post
           WHERE post.post_id = %s""",
        (id,)
    )
    post = cur.fetchone()
    cur.close()
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if post[1] != g.user[0]:
        abort(403)

    return post


@app.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    if load_logged_in_user():
        post = get_post(id)
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            error = None

            if not title:
                error = 'Title is required!'
            if error is not None:
                flash(error)
                return redirect(url_for('index'))
            else:
                conn = get_dbConn()
                cur = conn.cursor()
                cur.execute('UPDATE post SET title = %s, body = %s'
                            'WHERE post_id = %s',
                            (title, body, id)
                            )
                cur.close()
                conn.commit()
                return redirect(url_for('index'))
        else:
            return render_template('blog/update.html', post=post)
    else:
        error = 'Only loggedin users can insert posts!'
        flash(error)
        return redirect(url_for('login'))


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_dbConn()
    cur = conn.cursor()
    cur.execute('DELETE FROM post WHERE post_id = %s', (id,))
    conn.commit()
    return redirect(url_for('index'))


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
