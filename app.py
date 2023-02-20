from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://skfpfpfp:dA7tx6BzNTV5RogEQhzbejgOe4HpoUtz@tuffi.db.elephantsql.com/skfpfpfp"
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email}
    
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
    

# Create the table if it doesn't exist
with app.app_context():
    db.create_all()
    
    
    
#Create a home route
@app.route('/', methods=['GET'])
def home():
    return make_response(jsonify({"message": 'Welcome to the home page'}), 200)
    
# Create a test route
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({"message": "Test route and connection"}), 200)




# Create a user

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        username = data['username']
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message":f"User: {username} created successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"message": "An error occured while creating user"}), 500)

    

# Get all users
@app.route('/users', methods=['GET'])
def all_users():
    try:
        users = User.query.all()
        return make_response(jsonify({"users": [user.json() for user in users]}), 200)
    except Exception as e:
        return make_response(jsonify({"message": "An error occured while getting users"}), 500)
    
    
# Get a single user
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({"user": user.json()}), 200)
        return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "An error occured while getting user"}), 500)
    
    
# Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.update(user)
            db.session.commit()
            return make_response(jsonify({"message": "User updated successfully"}), 200)
        return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "An error occured while updating user"}), 500)
    
    
# Delete user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try: 
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"message": "User deleted successfully"}), 200)
        return make_response(jsonify({"message": "User not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"message": "An error occured while deleting user"}), 500)
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
