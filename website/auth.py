from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import hashlib

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', 'success')
            else:
                flash('Incorrect password, try again.', 'error')
        else:
            flash('Invalid email or password.', 'error')
    return render_template("login.html",boolean="")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'error')
        elif len(email) < 4:
            flash('Email must be at least 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be at least 2 characters', category='error')
        elif len(second_name) < 2:
            flash('First name must be at least 2 characters', category='error')
        elif len(password1) < 8:
            flash("Password must be at least 8 characters", category="error")
        elif password1 != password2:
            flash("Passwords don't match", category="error")
        else:
            hashed_password = generate_password_hash(password1, method='sha256')
            new_user = User(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")

