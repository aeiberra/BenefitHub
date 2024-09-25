from app import create_app, db
from app.models import User, Category, Benefit, Redemption
from app.seed_data import seed_data

app = create_app()

with app.app_context():
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Create all tables
    seed_data()  # Seed the database with new data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
