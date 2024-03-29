from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify
from models import User, db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token


auth_bp = Blueprint('auth_be', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter_by(username=data['username']).first
    if existing_user:
        return jsonify({'message': 'Username already taken'}), 400
    
    try:
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Failed to register user'}), 500
        

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=data['username'])
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid username or password'}), 401