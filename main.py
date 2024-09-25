from app import create_app, db
from app.models import User, Category, Benefit, Redemption
from app.seed_data import seed_data
import os

app = create_app()

with app.app_context():
    # Print database URL (without sensitive information)
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    if db_url:
        print(f"Database URL: {db_url.split('@')[1] if '@' in db_url else 'Set, but unable to parse'}")
    else:
        print("Database URL is not set")

    # Check if the database is empty
    if User.query.count() == 0:
        seed_data()  # Seed the database with initial data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
