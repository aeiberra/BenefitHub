from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.auth import bp
from app.models import User
from app import db
import logging

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('Invalid username')
            logging.warning(f"Login attempt with invalid username: {username}")
            return render_template('admin/login.html')
        if not user.check_password(password):
            flash('Invalid password')
            logging.warning(f"Failed login attempt for user: {username}")
            return render_template('admin/login.html')
        login_user(user)
        logging.info(f"Successful login for user: {username}")
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
