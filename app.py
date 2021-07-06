import os
import MySQLdb.cursors
from flask import Flask, render_template, request, session, redirect, url_for
from flask.helpers import send_file
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

app.secret_key = 'secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cococo'
app.config['MYSQL_DB'] = 'users'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

@app.route('/loacsv/',  methods=['GET', 'POST'])
def load():
    msg = 'Error.'
    if request.method == 'POST':
        msg = 'post'
        if 'file' in request.files:
            file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        msg = 'Archivo guardado correctamente...'
    return render_template('loadcsv.html', msg = msg)

@app.route('/show/', methods=['GET', 'POST'])
def redirect():
    return render_template('show.html')

@app.route('/showTab')
def show_files():
    content = os.listdir(app.config['UPLOAD_FOLDER'])
    files = []
    print(content)
    for file in content:
        print(os.path.join(app.config['UPLOAD_FOLDER']) + '/' + file) 
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER']) + '/' + file) and file.endswith('.csv'):
            files.append(file)
    print('aqui toy')
    print(files)
    return render_template('show.html', files=files)

if __name__ == '__main__':
    app.run(debug=True)