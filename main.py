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
        # Create all tables
        db.create_all()
        logging.info("All database tables have been created")

        # Always run seed_data to ensure admin user exists
        logging.info("Running seed_data function...")
        seed_data()

        # Verify admin user after seeding
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            logging.info(f"Admin user verified - Username: {admin_user.username}, ID: {admin_user.id}")
            # Test password verification
            test_password = 'admin123'
            is_password_correct = admin_user.check_password(test_password)
            logging.info(f"Is 'admin123' the correct password? {is_password_correct}")
        else:
            logging.error("Admin user not found in the database after seeding")

        # Print all users in the database
        users = User.query.all()
        logging.info("Users in the database:")
        for user in users:
            logging.info(f"Username: {user.username}, ID: {user.id}")

    except Exception as e:
        logging.error(f"Error occurred during database setup or seeding: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
