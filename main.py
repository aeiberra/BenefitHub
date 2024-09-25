from app import create_app, db
from app.models import User, Category, Benefit, Redemption
from app.seed_data import seed_data
import os
import logging

app = create_app()

with app.app_context():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Print database URL (without sensitive information)
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    if db_url:
        print(f"Database URL: {db_url.split('@')[1] if '@' in db_url else 'Set, but unable to parse'}")
    else:
        print("Database URL is not set")

    try:
        # Check if the database is empty
        if User.query.count() == 0 and Category.query.count() == 0 and Benefit.query.count() == 0:
            logging.info("Database is empty. Running seed_data function.")
            seed_data()  # Seed the database with initial data
        else:
            logging.info("Database already contains data. Skipping seed operation.")
    except Exception as e:
        logging.error(f"Error occurred while seeding the database: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
