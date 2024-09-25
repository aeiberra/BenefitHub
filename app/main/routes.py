from flask import render_template, request, jsonify
from app.main import bp
from app.models import Category, Benefit, Redemption
from app import db
import qrcode
import io
import base64

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
    benefit_id = request.form['benefit_id']
    dni = request.form['dni']
    
    benefit = Benefit.query.get_or_404(benefit_id)
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"Benefit: {benefit.name}, DNI: {dni}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert QR code to base64
    buffered = io.BytesIO()
    img.save(buffered)
    qr_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    # Save redemption
    redemption = Redemption(dni=dni, benefit_id=benefit_id, qr_code=qr_base64)
    db.session.add(redemption)
    db.session.commit()
    
    return jsonify({'qr_code': qr_base64})
