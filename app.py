from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import jwt

# token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithm="HS256")

USER = {'user': "", 'password': ''}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super_secret_key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Expense(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String, nullable=False)
  expense = db.Column(db.Float, nullable=False)

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
  try:
    data = request.get_json()
    username = data.get('user')
    password = data.get('password')

    if USER['user'] and USER['password']:
      return jsonify({'message': 'user has already been registered'})

    if not username or not password:
      return jsonify({'message': 'username or password field is empty'}), 402
    
    USER['user'] = data.get('user')
    USER['password'] = data.get('password')
    return jsonify({'message': 'created'}), 200
  except Exception as e:
    return jsonify({'message': e}), 402
  




if __name__ == "__main__":
  app.run(debug=True)