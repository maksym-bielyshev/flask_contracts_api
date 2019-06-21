from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
db = SQLAlchemy()


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer)
    project_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    rules = db.relationship('Rule', backref='contract', lazy=True)


class Rules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    square = db.Column(db.Float)
    rooms = db.Column(db.Integer)
    toilets = db.Column(db.Integer)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))


@app.route('/contracts', methods=['GET'])
def get_all_contracts():

    contracts = Contract.query.all()

    output = []

    for contract in contracts:
        contract_data = {}
        contract_data['public_id'] = contract.public_id
        contract_data['user_id'] = contract.user_id
        contract_data['project_id'] = contract.project_id
        contract_data['name'] = contract.name
        output.append(contract_data)

    return jsonify({'contracts' : output})


@app.route('/contracts/<public_id>', methods=['GET'])
def get_one_contract(public_id):

    contract = Contract.query.filter_by(public_id=public_id).first()

    if not contract:
        return jsonify({'message': 'No contract found'})

    contract_data = {}
    contract_data['public_id'] = contract.public_id
    contract_data['user_id'] = contract.user_id
    contract_data['project_id'] = contract.project_id
    contract_data['name'] = contract.name

    return jsonify({'contract' : contract_data})


@app.route('/contracts', methods=['POST'])
def create_contract():
    data = request.get_json()
    new_contract = Contract(public_id=str(uuid.uuid4()), user_id=data['user_id'], project_id=data['project_id'],
                            name=data['name'])
    db.session.add(new_contract)
    db.session.commit()

    return jsonify({'message': 'New contract created'})


@app.route('/contracts/public_id', methods=['PUT'])
def edit_contract(public_id):

    contract = Contract.query.filter_by(public_id=public_id).first()

    if not contract:
        return jsonify({'message': 'No contract found'})

    db.session.commit()

    return jsonify({'message': 'Contract was updated'})


@app.route('/contracts/<public_id>', methods=['DELETE'])
def delete_contract(public_id):

    contract = Contract.query.filter_by(public_id=public_id).first()

    if not contract:
        return jsonify({'message': 'No contract found'})

    db.session.delete(contract)
    db.session.commit()

    return jsonify({'message': 'Contract was deleted'})


@app.route('/rules/<rules_id>', methods=['POST'])
def create_rules(rules_id):
    data = request.get_json()

    new_rules = Rules(square=data['square'], rooms=data['rooms'], toilets=data['toilets'],
                      contract_id=data['contract_id'])

    db.session.add(new_rules)
    db.session.commit()

    return jsonify({'message': 'Rules created'})


@app.route('/rules/<rules_id>', methods=['DELETE'])
def delete_rules(rules_id):

    rules = Rules.query.filter_by(id=rules_id).first()

    if not rules:
        return jsonify({'message': 'No rules found'})

    db.session.delete(rules)
    db.session.commit()

    return jsonify({'message': 'Rules were deleted'})


if __name__ == '__main__':
    app.run(debug=True)
