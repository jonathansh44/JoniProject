# app/controllers/main.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@bp.route('/user/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        
        # Check for existing username/email
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('main.add_user'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('main.add_user'))
        
        # Create and save
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        
        flash('User added successfully')
        return redirect(url_for('main.index'))
        
    return render_template('add_user.html')

@bp.route('/user/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully')
    return redirect(url_for('main.index'))
