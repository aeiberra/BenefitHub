from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required
from app.admin import bp
from app.models import Benefit, Category, Redemption
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
def dashboard():
    benefits = Benefit.query.all()
    categories = Category.query.all()
    return render_template('admin/dashboard.html', benefits=benefits, categories=categories)

# Existing routes...

@bp.route('/category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        image_url = request.form['image_url']
        
        category = Category(name=name, image_url=image_url)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html')

@bp.route('/category/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form['name']
        category.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', category=category)

@bp.route('/category/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('admin.categories'))

@bp.route('/categories')
@login_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

# Existing routes...
