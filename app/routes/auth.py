from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard'))

        flash('Invalid username or password. Please try again.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template("auth/login.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm')
        email = request.form.get('email')

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'warning')
            return redirect(url_for('auth.register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered.', 'warning')
            return redirect(url_for('auth.register'))

        # Create and set hashed password via model's password_raw property
        new_user = User(username=username, email=email)
        new_user.password = password

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        flash('Registration successful. Welcome!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')
