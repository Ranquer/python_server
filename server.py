from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
# import hashliby
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("/index.html")

@app.route('/pylog', methods=['GET', 'POST'])
def login():
    msg = 'coso'
    
    if request.method == 'GET' and 'id_user' in request.form and 'password' in request.form:
        id_user = request.form['id_user']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id_user = %s AND password = %s',(id_user, password))
        account = cursor.fetchone()
        msg = 'colorido'
        if account:
            session['loggedin'] = True
            session['id_user'] = account['id_user']
            session['user_name'] = account['user_name']
            session['appointment'] = account['appointment']
            print('aqui si') 
            return 'Logged in successfully!'
        else:
            msg = 'cosa'
            print('ya estas')
    else:
        print('No jala tu codigo pagina miada regresame mis 46 horas')
    return render_template('index.html', msg=msg)
