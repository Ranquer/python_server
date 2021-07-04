from flask import Flask, render_template, request, session, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)

app.secret_key = 'secret_key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cococo'
app.config['MYSQL_DB'] = 'users'


mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pylog/', methods=['GET', 'POST'])
def log():
    msg = ""
    if request.method == 'POST' and 'id_user' in request.form and 'password' in request.form:
        id_user = request.form['id_user']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE id_user = %s AND password = %s', (id_user, password))
        account = cursor.fetchone()
        if account:
            session['logged'] = True
            session['id_user'] = account['id_user']
            session['employment'] = account['employment']
            if session['employment'] == 0:
                return render_template('loadcsv.html')
            elif session['employment'] == 1:
                msg = 'eres admin perro esperate'
            else:
                msg = 'Quien vergas eres perro :V'
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/loacsv',  methods=['GET', 'POST'])
def loacsv():

    return render_template('index.html', msg = 'msg')

if __name__ == '__main__':
    app.run(debug=True)