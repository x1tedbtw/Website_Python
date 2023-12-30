from flask import Blueprint, render_template, request, redirect

views = Blueprint('views', __name__)

@views.route('/') #decorator with root


def home():
    return render_template("home.html")