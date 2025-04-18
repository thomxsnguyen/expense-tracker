from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone

import jwt

# token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithm="HS256")
#thomxsnguyen, #thomas123

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGhvbXhzbmd1eWVuIn0.ZC6kmDkWC2YEcD7aVRORiRCifJ9t5el_91Mohj9kyw8"

#audge, #missaudreychang
app = Flask(__name__)

app.config['SECRET_KEY'] = 'super_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  expenses = db.relationship('Expense', back_populates='user')

  def view(self):
    return self.username, self.password_hash

class Expense(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String(50), nullable=False)
  description = db.Column(db.String(1000), nullable=False)
  price = db.Column(db.Float, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

  user = db.relationship('User', back_populates='expenses')

  def to_dict(self):
    return {
      'id': self.id, 'category': self.category, 'description': self.description, 'price': self.price
    }


@app.route('/')
def home():
  return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
  try:
    data = request.get_json()
    username = data.get('user')

    hash_password = generate_password_hash(data.get('password'))

    user = User(username=username, password_hash=hash_password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'created'}), 200
  except Exception as e:
    return jsonify({'error': str(e)}), 402
  

@app.route('/login', methods=['POST'])
def login():
  profile = request.get_json()
  username = profile.get('user')
  password = profile.get('password')
  print(username, password)

  user = User.query.filter_by(username=username).first()

  if user and check_password_hash(user.password_hash, password):
    token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": token}), 200
  
  return jsonify({"error": "invalid credentials"}), 401


@app.route('/expense', methods=['POST'])
def create_expense():
  profile = get_user_data()
  data =  request.get_json()

  username = profile['user']

  description = data.get('description')
  category = data.get('category')
  price = data.get('price')
  if description and category and price:
    user = db.session.query(User).filter_by(username=username).first()
    new_expense = Expense(description=description, category=category, price=price, user=user)
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "expense added"}), 200
  return jsonify({"message": "invalid body request"}), 401

@app.route('/expenses', methods=['GET'])
def view():
  profile = get_user_data()
  
  filter_type = request.args.get('filter')
  start_date = request.args.get('start')
  end_date = request.args.get('end')

  today = datetime.now(timezone.utc)

  if filter_type == "week":
    from_date = today - timedelta(days=7)
    to_date = today
  elif filter_type == "month":
    from_date = today - timedelta(days=30)
    to_date = today
  elif filter_type == "3months":
    from_date = today - timedelta(days=90)
    to_date = today
  elif filter_type == "custom":
    pass
  else:
    return jsonify({'ERROR': 'Invalid filter option'}), 400
  
  expenses = Expense.query.filter(
    Expense.user_id == profile.id,
    Expense.date >= from_date,
    Expense.date <= to_date
  ).all()

  return jsonify([expense.to_dict() for expense in expenses]), 200

  # username = profile['user']
  # user = User.query.filter_by(username=username).first()
  # expenses = [expense.to_dict() for expense in user.expenses]
  # return jsonify({"message": expenses}), 200

def get_user_data():
  header = request.headers.get('Authorization')

  if not header:
    return jsonify({"message": "header is missing"}), 401
  
  try:
    token = header.split(" ")[1]
  except Exception as e:
    return jsonify({"error": str(e)})
  
  try:
    profile = jwt.decode(token, app.config['SECRET_KEY'],  algorithms=['HS256'])
    return profile
  except Exception as e:
    return f'ERROR: {e}'
  




if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True)