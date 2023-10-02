from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure random key
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['SERVER_NAME'] = "dev.igormartin.es"
# app.config['SESSION_COOKIE_DOMAIN'] = "127.0.0.1:5000"

app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['CORS_METHODS'] = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']
app.config['CORS_ORIGINS'] = '*'
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

jwt = JWTManager(app)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

users = {
    "username": "password"
}

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Perform authentication here (e.g., check against a database)
    # If authentication succeeds, generate JWT and return it

    if username in users and users[username] == password:
        access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=1))
        response = make_response(jsonify({'message': 'Login succesful'}), 200)
        response.set_cookie('access_token_cookie', access_token, secure=True, path='/', samesite='None')
        return response
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Access granted for user: {current_user}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
