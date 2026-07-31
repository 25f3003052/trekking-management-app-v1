from flask import render_template, redirect, session, request, flash
from app import app
from models import * 
from datetime import datetime, date as date_class


# home page route
@app.route('/')
def home():
    return render_template('index.html')
