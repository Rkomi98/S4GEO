#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 23:54:08 2019

@author: Mirko
"""

from psycopg2 import (
    connect
)
# It has to be deleted at the end of the application.
cleanup = (
    'DROP TABLE IF EXISTS blog_user CASCADE',
)

commands = (
    """
        CREATE TABLE blog_user (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) UNIQUE NOT NULL,
            user_password VARCHAR(255) NOT NULL
        )
        """,)
#TIME WITH TIME ZONE
sqlCommands = (
    'INSERT INTO blog_user (user_name, user_password) VALUES (%s, %s) RETURNING user_id',
)
conn = connect("dbname=S4G user=postgres password=Gram2021")
cur = conn.cursor()
for command in cleanup:
    cur.execute(command)
for command in commands:
    cur.execute(command)
    print('execute command')
cur.execute(sqlCommands[0], ('Rome', 'Italy'))
userId = cur.fetchone()[0]
print(cur.fetchall())

cur.close()
conn.commit()
conn.close()
