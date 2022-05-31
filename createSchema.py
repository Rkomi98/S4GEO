#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 23:54:08 2019

@author: elisabettadinitto
"""

from psycopg2 import (
    connect
)
# It has to be deleted at the end of the application.
cleanup = (
    'DROP TABLE IF EXISTS blog_user CASCADE',
    'DROP TABLE IF EXISTS post',
    'DROP TABLE IF EXISTS city'
)

commands = (
    """
        CREATE TABLE blog_user (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) UNIQUE NOT NULL,
            user_password VARCHAR(255) NOT NULL
        )
        """,
    """ 
        CREATE TABLE post (
                post_id SERIAL PRIMARY KEY,
                author_id INTEGER NOT NULL,
                created TIMESTAMP DEFAULT NOW(),
                title VARCHAR(350) NOT NULL,
                body VARCHAR(500) NOT NULL,
                FOREIGN KEY (author_id)
                    REFERENCES blog_user (user_id)
        )
        """,
        """
        CREATE TABLE city (
            city_id SERIAL PRIMARY KEY,
            author_id INTEGER NOT NULL,
            name_city VARCHAR,
        	air_quality INTEGER ,
            carbon_monoxyde REAL, 
            relative_humidity REAL, 
            nitrogen_dioxide REAL,
            ozone REAL,
            atmospheric_pressure REAL,
            pm10 REAL,
            pm25 REAL,
            so2 REAL,
            temperature REAL,
            wind REAL,
            time_zone VARCHAR(350),
            latitude REAL,
            longitude REAL,
            geometry geometry,
            FOREIGN KEY (author_id)
                REFERENCES blog_user (user_id)
            )
        """)
#TIME WITH TIME ZONE
sqlCommands = (
    'INSERT INTO blog_user (user_name, user_password) VALUES (%s, %s) RETURNING user_id',
    'INSERT INTO post (title, body, author_id) VALUES (%s, %s, %s)',
    'INSERT INTO city (name_city, air_quality, carbon_monoxyde, relative_humidity, nitrogen_dioxide, ozone,atmospheric_pressure,pm10,pm25,so2,temperature,wind,time_zone,latitude,longitude,geometry,author_id) VALUES(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
)
conn = connect("dbname=s4g user=postgres password=Soft1234")
cur = conn.cursor()
for command in cleanup:
    cur.execute(command)
for command in commands:
    cur.execute(command)
    print('execute command')
cur.execute(sqlCommands[0], ('Giuseppe', '3ety3e7'))
userId = cur.fetchone()[0]
cur.execute(sqlCommands[1], ('My First Post', 'This is the post body', userId))
cur.execute('SELECT * FROM post')
cur.execute(sqlCommands[2], ('Paris',
                             51,
                             0.1,
                             84.3,
                             35.6,
                             14.4,
                             1000.7,
                             6,
                             51,
                             0.6,
                             18.1,
                             1.3,
                             '2022-05-23 10:00:00+02:00',
                             48.856614,
                             2.352222,
                             'POINT (2.35222 48.85661)', 
                             userId)
            )
cur.execute('SELECT * FROM city')
print(cur.fetchall())

cur.close()
conn.commit()
conn.close()
