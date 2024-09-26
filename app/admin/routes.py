from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.admin import bp
from app.models import Benefit, Category, Redemption
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta
import logging

@bp.route('/dashboard')
@login_required
def dashboard():
    benefits = Benefit.query.all()
    categories = Category.query.order_by(Category.order).all()
    return render_template('admin/dashboard.html', benefits=benefits, categories=categories)

@bp.route('/benefit/add', methods=['GET', 'POST'])
@login_required
def add_benefit():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']
        company = request.form['company']
        category_id = request.form['category_id']
        featured = 'featured' in request.form
        
        benefit = Benefit(name=name, description=description, image_url=image_url,
                          company=company, category_id=category_id, featured=featured)
        db.session.add(benefit)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    
    categories = Category.query.all()
    return render_template('admin/benefit_form.html', categories=categories)

@bp.route('/benefit/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_benefit(id):
    benefit = Benefit.query.get_or_404(id)
    if request.method == 'POST':
        benefit.name = request.form['name']
        benefit.description = request.form['description']
        benefit.image_url = request.form['image_url']
        benefit.company = request.form['company']
        benefit.category_id = request.form['category_id']
        benefit.featured = 'featured' in request.form
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    
    categories = Category.query.all()
    return render_template('admin/benefit_form.html', benefit=benefit, categories=categories)

@bp.route('/benefit/<int:id>/delete', methods=['POST'])
@login_required
def delete_benefit(id):
    benefit = Benefit.query.get_or_404(id)
    db.session.delete(benefit)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

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
    categories = Category.query.order_by(Category.order).all()
    logging.info(f"Categories being sent to template: {[(c.id, c.name, c.order) for c in categories]}")
    return render_template('admin/categories.html', categories=categories)

@bp.route('/benefit/<int:id>/toggle_featured', methods=['POST'])
@login_required
def toggle_featured(id):
    benefit = Benefit.query.get_or_404(id)
    benefit.featured = not benefit.featured
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@bp.route('/analytics')
@login_required
def analytics():
    return render_template('admin/analytics.html')

@bp.route('/api/analytics')
@login_required
def api_analytics():
    logging.info(f"User {current_user.username} accessing analytics API")
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # Daily redemptions query
    daily_redemptions = db.session.query(
        func.date(Redemption.timestamp).label('date'),
        func.count(Redemption.id).label('count')
    ).filter(Redemption.timestamp >= seven_days_ago).group_by(func.date(Redemption.timestamp)).all()
    logging.info(f"Daily redemptions query result: {daily_redemptions}")

    # Top benefits query
    top_benefits = db.session.query(
        Benefit.name,
        func.count(Redemption.id).label('count')
    ).join(Redemption).group_by(Benefit.id).order_by(func.count(Redemption.id).desc()).limit(5).all()
    logging.info(f"Top benefits query result: {top_benefits}")

    # Category redemptions query
    category_redemptions = db.session.query(
        Category.name,
        func.count(Redemption.id).label('count')
    ).select_from(Category).join(Benefit, Category.id == Benefit.category_id).join(Redemption, Benefit.id == Redemption.benefit_id).group_by(Category.id).all()
    logging.info(f"Category redemptions query result: {category_redemptions}")

    response_data = {
        'daily_redemptions': [{'date': str(item.date), 'count': item.count} for item in daily_redemptions],
        'top_benefits': [{'name': item.name, 'count': item.count} for item in top_benefits],
        'category_redemptions': [{'name': item.name, 'count': item.count} for item in category_redemptions]
    }
    logging.info(f"Analytics API response: {response_data}")
    return jsonify(response_data)

@bp.route('/update_category_order', methods=['POST'])
@login_required
def update_category_order():
    data = request.json
    category_id = data.get('category_id')
    new_order = data.get('new_order')
    
    logging.info(f"Received request to update category order: category_id={category_id}, new_order={new_order}")
    
    if category_id is None or new_order is None:
        logging.error(f"Invalid data received: category_id={category_id}, new_order={new_order}")
        return jsonify({'success': False, 'error': 'Invalid data'}), 400
    
    try:
        categories = Category.query.order_by(Category.order).all()
        logging.info(f"All categories: {[{c.id: c.name} for c in categories]}")
        
        category_to_move = Category.query.get(category_id)
        
        if category_to_move is None:
            logging.error(f"Category not found: id={category_id}")
            return jsonify({'success': False, 'error': 'Category not found'}), 404
        
        logging.info(f"Category to move: id={category_to_move.id}, name={category_to_move.name}")
        
        current_index = categories.index(category_to_move)
        categories.insert(new_order, categories.pop(current_index))
        
        for index, category in enumerate(categories):
            category.order = index
            db.session.add(category)
        
        db.session.commit()
        logging.info(f"Category order updated successfully: id={category_id}, new_order={new_order}")
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error updating category order: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
