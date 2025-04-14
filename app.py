from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

import jwt

# token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithm="HS256")


app = Flask(__name__)

app.config['SECRET_KEY'] = 'super_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  expenses = db.relationship('Expense', backref="user", lazy=True)

  def view(self):
    return self.username, self.password_hash
  

  
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
    password = generate_password_hash(data.get('password'))

    user = User(username=username)
    user.password = password

    db.session.commit()
    
    return jsonify({'message': 'created'}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 402
  

@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')

  user = User.query.filter_by(username=username).first()

  if user.password == password:
    token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithim="HS256")
    return jsonify({"token": token}), 200
  
  return jsonify({"error": "invalid credentials"}), 401

@app.route('/expense', methods=['POST'])
def create_expense():
  header = request.headers.get('Authorization')

  if not header:
    return jsonify({"message": "header is missing"}), 401
  
  try:
    token = header.split(" ")[1]
  except Exception as e:
    return jsonify({"error": str(e)})
  
  try:
    data = jwt.decode(token, app.config['SECRET_KEY'],  algorithms=['HS256'])
    return jsonify({"data": data}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 401

  




if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)