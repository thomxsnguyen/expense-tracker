from flask import Flask, render_template, jsonify, request
import jwt

# token = jwt.encode({'user': username}, app.config['SECRET_KEY'], algorithm="HS256")

USER = {'user': "", 'password': ''}


app = Flask(__name__)

@app.route('/')
def home():
  render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  if not USER
  USER['user'] = data.get('user')
  USER['password'] = data.get('password')

  return jsonify({'message': "registered"}), 200






if __name__ == "__main__":
  app.run(debug=True)