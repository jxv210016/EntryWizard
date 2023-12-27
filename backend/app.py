from flask import Flask, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return 'Welcome to the main page!'

@app.route('/login/discord')
def discord_login():
    params = {
        'client_id': os.getenv('DISCORD_CLIENT_ID'),
        'redirect_uri': os.getenv('DISCORD_REDIRECT_URI'),
        'response_type': 'code',
        'scope': 'identify email'
    }
    discord_login_url = 'https://discord.com/api/oauth2/authorize?' + requests.compat.urlencode(params)
    return redirect(discord_login_url)

@app.route('/login/discord/callback')
def discord_callback():
    code = request.args.get('code')
    if code:
        data = {
            'client_id': os.getenv('DISCORD_CLIENT_ID'),
            'client_secret': os.getenv('DISCORD_CLIENT_SECRET'),
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': os.getenv('DISCORD_REDIRECT_URI')
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        token_response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
        token_response.raise_for_status()
        access_token = token_response.json().get('access_token')

        user_response = requests.get('https://discord.com/api/users/@me', headers={'Authorization': f'Bearer {access_token}'})
        user_response.raise_for_status()
        user_data = user_response.json()

        user = User.query.filter_by(discord_id=user_data['id']).first()
        if not user:
            user = User(discord_id=user_data['id'], username=user_data['username'], email=user_data.get('email'))
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for('index'))
    else:
        return jsonify({'error': 'Authorization code not provided'}), 400

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
