from flask import render_template, request, jsonify, url_for, abort
from app.main import bp
from app.models import Category, Benefit, Redemption
from app import db
import qrcode
import io
import base64
from datetime import datetime

@bp.route('/')
def index():
    categories = Category.query.all()
    featured_benefits = Benefit.query.filter_by(featured=True).limit(5).all()
    return render_template('index.html', categories=categories, featured_benefits=featured_benefits)

@bp.route('/category/<int:id>')
def category(id):
    category = Category.query.get_or_404(id)
    benefits = category.benefits.all()
    return render_template('category.html', category=category, benefits=benefits)

@bp.route('/benefit/<int:id>')
def benefit(id):
    benefit = Benefit.query.get_or_404(id)
    return render_template('benefit.html', benefit=benefit)

@bp.route('/redeem', methods=['POST'])
def redeem():
    benefit_id = request.form.get('benefit_id')
    dni = request.form.get('dni')
    
    if not benefit_id or not dni:
        return jsonify({'error': 'Benefit ID and DNI are required'}), 400
    
    try:
        benefit = Benefit.query.get_or_404(benefit_id)
        
        # Create redemption record
        redemption = Redemption(dni=dni, benefit_id=benefit_id)
        db.session.add(redemption)
        db.session.commit()
        
        # Generate QR code with unique identifier
        qr_data = url_for('main.confirm_redemption', unique_id=redemption.unique_id, _external=True)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert QR code to base64
        buffered = io.BytesIO()
        img.save(buffered)
        qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Update redemption record with QR code
        redemption.qr_code = qr_base64
        db.session.commit()
        
        return jsonify({'qr_code': qr_base64})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/confirm_redemption/<unique_id>')
def confirm_redemption(unique_id):
    redemption = Redemption.query.filter_by(unique_id=unique_id).first_or_404()
    
    if not redemption.is_scanned:
        redemption.is_scanned = True
        redemption.scanned_timestamp = datetime.utcnow()
        db.session.commit()
        message = "¡Beneficio canjeado exitosamente!"
    else:
        message = "Este beneficio ya ha sido canjeado."
    
    return render_template('confirm_redemption.html', redemption=redemption, message=message)
