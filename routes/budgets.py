from flask import Blueprint, request, jsonify
from models import db, Budget
from flask_jwt_extended import jwt_required, get_jwt_identity

budgets_bp = Blueprint('budgets_bp', __name__)

#Create
@budgets_bp.route('/add', methods=['POST'])
@jwt_required()
def add_budget():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_budget = Budget(user_id=user_id, category=data['category'], limit=data['limit'])
    db.session.add(new_budget)
    db.session.commit()
    return jsonify({"message": "Budget added successfully"}), 201

#Read
@budgets_bp.route('/all', methods=['GET'])
@jwt_required()
def get_budgets():
    user_id = get_jwt_identity()
    budgets = Budget.query.filter_by(user_id=user_id).all()
    return jsonify([budget.to_dict()for budget in budgets]), 200

#Update
@budgets_bp.route('/update/<int:budget_id>', methods=['PUT'])
@jwt_required()
def update_budget(budget_id):
    user_id = get_jwt_identity()
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    if budget:
        data = request.get_json()
        budget.category = data.get('category', budget.category)
        budget.limit = data.get('limit', budget.limit)
        db.session.commit()
        return jsonify({'message': 'Budget update successfully'}), 200
    else:
        return jsonify({'message': 'Budget not found'}), 404
    
#Delete
@budgets_bp.route('/delete/<int:budget_id>', methods=['DELETE'])
@jwt_required()
def delete_budget(budget_id):
    user_id = get_jwt_identity()
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    if budget:
        db.session.delete(budget)
        db.session.commit()
        return jsonify({'message': 'Budget deleted successfully'}), 200
    else: 
        return jsonify({'message': 'Budget not found'}), 404