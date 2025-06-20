from app import app, users_collection
from flask import render_template, request, jsonify
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

from app.forms import LoginForm


@app.route('/')
@app.route('/home')
def home():
    user = {'username': 'admin', 'password': '<PASSWORD>'}
    users = list(users_collection.find())
    return render_template('index.html', user=user, title='Home', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    try:
        user_data = request.get_json()

        if 'username' not in user_data or 'email' not in user_data or 'password' not in user_data:
            return jsonify({'error': 'Missing required fields (username, email, password)'}), 400

        hashed_password = generate_password_hash(user_data['password'])

        user_id = users_collection.insert_one({
            'username': user_data['username'],
            'email': user_data['email'],
            'password': hashed_password
        }).inserted_id

        user_data['_id'] = str(user_id)

        return jsonify({"message": "User created successfully", "user": user_data['_id']}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = list(users_collection.find())
        for user in users:
            user['_id'] = str(user['_id'])
        return jsonify({'users': users}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    return render_template('login.html', form=form, title='Sign In')
