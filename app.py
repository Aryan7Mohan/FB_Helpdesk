from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
'''
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
'''

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/fb_helpdesk'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''


# we do this so we dont get warning in console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'


class user_info(UserMixin, db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), unique=True)
    password = db.Column(db.Text())

    def __init__(self, username, password):
        self.username = username
        self.password = password

# to login with user id or something, its necessary


@login_manager.user_loader
def load_user(user_id):
    return user_info.query.get(int(user_id))


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        print(username, password)

        # to check if username already exists or not
        if db.session.query(user_info).filter(user_info.username == username).count() == 0:
            data = user_info(username, password)
            print(data)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('index'))
        print("user already exists")
        return render_template('index.html')

    return render_template('register.html')

# login


@app.route('/submit', methods=['POST'])
def submit():

    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        print(username, password)

        # to check if username already exists or not
        if user_info.query.filter(user_info.username == username and user_info.password == password).count() != 0:
            print("it works")
            user = user_info.query.filter_by(
                username=username).first()
            print(user)
            login_user(user)

            return redirect(url_for('connect'))
        else:
            print("wrong credentials")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "you are logged out!"


@app.route('/connect')
@login_required
def connect():

    return render_template('connect.html')


if __name__ == '__main__':
    app.run()
