from flask import Blueprint, request, jsonify
from models import db, Transaction
from flask_jwt_extended import jwt_required, get_jwt_identity

transactions_bp = Blueprint('transactions_bp', __name__)

#Create
@transactions_bp.route('/add', methods=['POST'])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_transaction = Transaction(user_id=user_id, amount=data['amount'], category=data['category'], data=data['data'])
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction added successfully"}), 201

#Read
@transactions_bp.route('/all', methods=['GET'])
@jwt_required()
def get_transaction():
    user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    return jsonify([transaction.to_dict() for transaction in transactions]), 200

#Update
@transactions_bp.route('/update/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if transaction:
        data = request.get_json()
        transaction.amount = data.get('amount', transaction.amount)
        transaction.category = data.get('category', transaction.category)
        transaction.date = data.get('date', transaction.category)
        db.session.commit()
        return jsonify({"message": "Transaction updated successfully"}), 200
    else:
        return jsonify({'message': "Transaction not found"}), 404
    
#Delete
@transactions_bp.route('/delete/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'message': "Transaction deleted successfully"}), 200
    else:
        return jsonify({"message": "Transaction not found"}), 404