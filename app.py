from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from services.api_service import fetch_codeforces_data, fetch_leetcode_data, fetch_codechef_data
from services.user_service import get_user_data, update_user_data, authenticate_user
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        codeforces_handle = request.form.get('codeforces_handle', '')
        leetcode_handle = request.form.get('leetcode_handle', '')
        codechef_handle = request.form.get('codechef_handle', '')

        # Create user and save platform handles
        user_id = create_user(username, password, {
            'codeforces': codeforces_handle,
            'leetcode': leetcode_handle,
            'codechef': codechef_handle
        })

        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            flash('Registration successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username already exists', 'danger')

    return render_template('login.html', register=True)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_data = get_user_data(session['user_id'])

    # Fetch data from competitive programming platforms
    codeforces_data = fetch_codeforces_data(user_data.get('handles', {}).get('codeforces', ''))
    leetcode_data = fetch_leetcode_data(user_data.get('handles', {}).get('leetcode', ''))
    codechef_data = fetch_codechef_data(user_data.get('handles', {}).get('codechef', ''))

    # Combine data for visualization
    platform_data = {
        'codeforces': codeforces_data,
        'leetcode': leetcode_data,
        'codechef': codechef_data
    }

    return render_template('dashboard.html',
                           user=user_data,
                           platform_data=platform_data)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_data = get_user_data(session['user_id'])

    if request.method == 'POST':
        # Update user handles
        handles = {
            'codeforces': request.form.get('codeforces_handle', ''),
            'leetcode': request.form.get('leetcode_handle', ''),
            'codechef': request.form.get('codechef_handle', '')
        }

        update_user_data(session['user_id'], {'handles': handles})
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=user_data)


@app.route('/api/refresh_data')
def refresh_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    user_data = get_user_data(session['user_id'])

    # Fetch fresh data from platforms
    codeforces_data = fetch_codeforces_data(user_data.get('handles', {}).get('codeforces', ''))
    leetcode_data = fetch_leetcode_data(user_data.get('handles', {}).get('leetcode', ''))
    codechef_data = fetch_codechef_data(user_data.get('handles', {}).get('codechef', ''))

    return jsonify({
        'codeforces': codeforces_data,
        'leetcode': leetcode_data,
        'codechef': codechef_data
    })


def create_user(username, password, handles=None):
    # Simple user creation function (would use a database in production)
    # In a real app, you would hash the password
    # This is just for demonstration purposes
    user_id = '123456'  # In reality, this would be generated
    user_data = {
        'id': user_id,
        'username': username,
        'password': password,  # In reality, this would be hashed
        'handles': handles or {}
    }
    update_user_data(user_id, user_data)
    return user_id


if __name__ == '__main__':
    app.run(debug=True)