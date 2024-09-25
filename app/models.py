from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    benefits = db.relationship('Benefit', backref='category', lazy='dynamic')

class Benefit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(256))
    company = db.Column(db.String(128))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    redemptions = db.relationship('Redemption', backref='benefit', lazy='dynamic')
    featured = db.Column(db.Boolean, default=False)  # New field for featured benefits

class Redemption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.String(20))
    benefit_id = db.Column(db.Integer, db.ForeignKey('benefit.id'))
    qr_code = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())
