from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

import jwt

# token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithm="HS256")

USER = {'user': "", 'password': ''}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  expenses = db.relationship('Expenses', backref="user", lazy=True)
  
class Expense(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String(50), nullable=False)
  description = db.Column(db.String(100), nullable=False)
  price = db.Column(db.Float, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)




@app.route('/')
def home():
  return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
  try:
    data = request.get_json()
    username = data.get('user')
    password = data.get('password')

    
    return jsonify({'message': 'created'}), 200
  except Exception as e:
    return jsonify({'error': e}), 402
  

@app.route('/login', methods=['POST'])
def login():
  try:
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == USER['username'] and password == USER['password']:
      token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithim="HS256")
      return jsonify({'token': token}), 200
    return jsonify({'message': 'invalid credentials'}), 402
  except Exception as e:
    return jsonify({'error': e})


  




if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)