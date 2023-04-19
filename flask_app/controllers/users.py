from flask_app import app
from flask import render_template, redirect, request, session, flash



@app.route('/')
def index_page():
    return render_template('index.html')
