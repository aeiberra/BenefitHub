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

@bp.route('/benefit', methods=['GET', 'POST'])
@login_required
def add_benefit():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']
        company = request.form['company']
        category_id = request.form['category_id']
        
        benefit = Benefit(name=name, description=description, image_url=image_url,
                          company=company, category_id=category_id)
        db.session.add(benefit)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    
    categories = Category.query.all()
    return render_template('admin/benefit_form.html', categories=categories)

@bp.route('/benefit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_benefit(id):
    benefit = Benefit.query.get_or_404(id)
    if request.method == 'POST':
        benefit.name = request.form['name']
        benefit.description = request.form['description']
        benefit.image_url = request.form['image_url']
        benefit.company = request.form['company']
        benefit.category_id = request.form['category_id']
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

@bp.route('/stats')
@login_required
def stats():
    redemptions = Redemption.query.all()
    stats = {
        'total_redemptions': len(redemptions),
        'top_benefits': Benefit.query.join(Redemption).group_by(Benefit.id).order_by(db.func.count(Redemption.id).desc()).limit(5).all()
    }
    return jsonify(stats)

@bp.route('/analytics')
@login_required
def analytics():
    return render_template('admin/analytics.html')

@bp.route('/api/analytics')
@login_required
def api_analytics():
    # Get data for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Total redemptions per day
    daily_redemptions = db.session.query(
        func.date(Redemption.timestamp).label('date'),
        func.count(Redemption.id).label('count')
    ).filter(Redemption.timestamp.between(start_date, end_date))\
     .group_by(func.date(Redemption.timestamp))\
     .order_by(func.date(Redemption.timestamp)).all()

    # Top 5 benefits
    top_benefits = db.session.query(
        Benefit.name,
        func.count(Redemption.id).label('count')
    ).join(Redemption)\
     .filter(Redemption.timestamp.between(start_date, end_date))\
     .group_by(Benefit.id)\
     .order_by(func.count(Redemption.id).desc())\
     .limit(5).all()

    # Redemptions by category
    category_redemptions = db.session.query(
        Category.name,
        func.count(Redemption.id).label('count')
    ).join(Benefit, Benefit.category_id == Category.id)\
     .join(Redemption)\
     .filter(Redemption.timestamp.between(start_date, end_date))\
     .group_by(Category.id)\
     .order_by(func.count(Redemption.id).desc()).all()

    return jsonify({
        'daily_redemptions': [{'date': str(r.date), 'count': r.count} for r in daily_redemptions],
        'top_benefits': [{'name': b.name, 'count': b.count} for b in top_benefits],
        'category_redemptions': [{'name': c.name, 'count': c.count} for c in category_redemptions]
    })
