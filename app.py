from flask import Flask, config, render_template, request, url_for, flash, redirect
from flask_mail import Mail, Message
import flask
from lib.key import Key
from lib.dbclient import DbClient
import os


conf_email = os.environ.get('conf_email', None)
conf_password = os.environ.get('conf_password', None)
conf_key = os.environ.get('conf_key', None)


# from config import  * #Used on local machine


app = Flask(__name__)

app.debug = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = conf_email
app.config['MAIL_PASSWORD'] = conf_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.secret_key = 'secret'
key = Key()
database_client = DbClient('users.db')

def send_email(user, message):
    msg = Message('Hello', sender = conf_email, recipients = [user])
    msg.body = "Follow this link to login to the site:\n\n"
    msg.body += message
    mail.send(msg)
    return f'Message sent to {user}'


@app.route('/login')
def hello():
    key = request.args.get('key')
    if len(database_client.get_key(key)):
        name = database_client.get_key(key)
        count = database_client.add_count(key)
        return f'Hello dear {name[0][0]} you visited this url {count} times!'
    else:
        return 'Who are you?'
    

@app.route('/admin',  methods=('GET', 'POST'))
def admin():
    key = request.args.get('key')
    if request.method =='POST':
        user_key = request.form['key']
        database_client.remove_user(user_key)
    if key == conf_key:
        records = database_client.get_admin_info()
        database_client.db_connection.close()
        return render_template('admin.html', records=records)
    else:
        return 'Who are you?'
    



@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        _key = key.build_key()
        if not database_client.add_new_user(name, email, _key):
            flash(f'User with e-mail {email} already exists', 'message')
            
        else:
            send_email(email, ''.join([flask.request.host_url, 'login' , '?&key=', _key]))
        
        database_client.db_connection.close()
    return render_template('register.html')


@app.route('/')
def redirect_to_register():
    return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(host= '0.0.0.0')