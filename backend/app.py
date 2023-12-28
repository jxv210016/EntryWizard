from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS  # Make sure flask_cors is imported

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100))
    unit_size = db.Column(db.Integer, default=0)

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@app.route('/unit', methods=['POST'])
@jwt_required()
def update_unit():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    new_unit_size = request.json.get('unit_size', None)
    if new_unit_size is not None:
        user.unit_size = new_unit_size
        db.session.commit()
        return jsonify({"msg": "Unit size updated"}), 200
    return jsonify({"msg": "No new unit size provided"}), 400

@app.route('/toggle_task', methods=['POST'])
@jwt_required()
def toggle_task():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    # This should actually toggle the task in your application logic
    user.task_running = not user.task_running  # Assuming you have a task_running column
    db.session.commit()
    return jsonify({"new_status": user.task_running}), 200

@app.route('/get_unit_size', methods=['GET'])
@jwt_required()
def get_unit_size():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    return jsonify({"unit_size": user.unit_size}), 200

@app.route('/get_task_status', methods=['GET'])
@jwt_required()
def get_task_status():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()
    return jsonify({"task_status": user.task_running}), 200  # Assuming task_running column

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
