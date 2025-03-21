import os
import json
from pathlib import Path

# In a real application, you would use a database instead of file storage
# This is a simplified implementation for demonstration purposes
DATA_DIR = Path('./data')
DATA_DIR.mkdir(exist_ok=True)


def get_user_data(user_id):
    """Get user data from storage"""
    user_file = DATA_DIR / f"user_{user_id}.json"

    if not user_file.exists():
        return None

    try:
        with open(user_file, 'r') as f:
            return json.load(f)
    except Exception:
        return None


def update_user_data(user_id, data):
    """Update user data in storage"""
    user_file = DATA_DIR / f"user_{user_id}.json"

    try:
        # If the file exists, load and update the existing data
        if user_file.exists():
            with open(user_file, 'r') as f:
                existing_data = json.load(f)
                # Update nested dictionaries properly
                for key, value in data.items():
                    if isinstance(value, dict) and key in existing_data and isinstance(existing_data[key], dict):
                        existing_data[key].update(value)
                    else:
                        existing_data[key] = value
            data_to_save = existing_data
        else:
            data_to_save = data

        with open(user_file, 'w') as f:
            json.dump(data_to_save, f, indent=2)
        return True
    except Exception as e:
        print(f"Error updating user data: {str(e)}")
        return False


def authenticate_user(username, password):
    """Authenticate a user"""
    # In a real application, you would query a database and use proper password hashing
    # This is a simplified implementation for demonstration purposes

    # For demo purposes, we'll accept a default user
    if username == "demo" and password == "password":
        return {
            'id': '123456',
            'username': 'demo',
            'handles': {
                'codeforces': 'tourist',
                'leetcode': 'tourist',
                'codechef': 'tourist'
            }
        }

    # Check all user files for matching credentials
    for file in DATA_DIR.glob("user_*.json"):
        try:
            with open(file, 'r') as f:
                user_data = json.load(f)
                if user_data.get('username') == username and user_data.get('password') == password:
                    return user_data
        except Exception:
            continue

    return None


def get_all_users():
    """Get all users (admin function)"""
    users = []
    for file in DATA_DIR.glob("user_*.json"):
        try:
            with open(file, 'r') as f:
                user_data = json.load(f)
                # Don't include password in the returned data
                if 'password' in user_data:
                    del user_data['password']
                users.append(user_data)
        except Exception:
            continue

    return users