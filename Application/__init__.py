# -*- coding: utf-8 -*-
"""
Created on Mon May 16 13:36:53 2022

@author: mirko
"""

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['NikilovesFlorence']
    
    return app