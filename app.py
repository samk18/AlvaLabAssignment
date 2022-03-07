from email.policy import default
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from datetime import datetime
import psycopg2
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Transaction Class/Model
class Transaction(db.Model):
  transaction_id = db.Column(db.Integer, primary_key=True)
  account_id = db.Column(db.String(100), unique=True)
  amount = db.Column(db.Integer)
  date_created = db.Column(db.DateTime, default =datetime.utcnow)

  def __init__(self, account_id, amount):
    self.account_id = account_id
    self.amount = amount

# Transaction Schema
class TransactionSchema(ma.Schema):
  class Meta:
    fields = ('transaction_id', 'account_id', 'amount', 'date_created')

# Init schema
transaction_schema = TransactionSchema(many=False)
transactions_schema = TransactionSchema(many=True)

@app.route("/ping")
def health():
    return "The service is up and running.", 200

# Create a Transaction
@app.route('/transactions', methods=['POST'])
def add_transaction():
 
 try:
   account_id = request.json['account_id']
   amount = request.json['amount']

   new_Transaction = Transaction(account_id, amount)

   db.session.add(new_Transaction)
   db.session.commit()

   return transaction_schema.jsonify(new_Transaction), 201

 except Exception as e:
   return jsonify({"Error": "409 Exists Already"})

# Get All Transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
  all_transactions = Transaction.query.all()
  result = transactions_schema.dump(all_transactions) 
  return jsonify(result)

# Get Single Transactions
@app.route('/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
 
 try:
   transaction = Transaction.query.get(transaction_id)
   return transaction_schema.jsonify(transaction)

 except Exception as e:
   return jsonify({"Error": "404 Trnasaction not found"})


# Get Single Accounts
@app.route('/accounts/<account_id>', methods=['GET'])
def get_account(account_id):
  try:
   account = Transaction.query \
        .filter(Transaction.account_id == account_id) \
        .one_or_none()
   if account is not None:
    return jsonify({'account_id':account.account_id, 'balance':account.amount})
   else:
    return jsonify({"Error": "404 Account not found"}) 
  except Exception as e:
   return jsonify({"Error": "400 account_id missing or has incorrect type"})

# Update a Transaction
@app.route('/transaction/<id>', methods=['PUT'])
def update_transaction(id):
  transaction = Transaction.query.get(id)

  price = request.json['amount']
  
  transaction.amount = price
  db.session.commit()

  return transaction_schema.jsonify(transaction)

# Delete Transaction
@app.route('/transaction/<id>', methods=['DELETE'])
def delete_transaction(id):
  transaction = Transaction.query.get(id)
  db.session.delete(transaction)
  db.session.commit()

  return transaction_schema.jsonify(transaction)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)