import os
from app import db, create_app
from app.models import Category, Benefit, User
import psycopg2
import logging

def seed_data():
    app = create_app()
    with app.app_context():
        # Configure logging
        logging.basicConfig(level=logging.INFO)

        # Test PostgreSQL connection
        try:
            conn = psycopg2.connect(
                host=os.environ.get('PGHOST'),
                database=os.environ.get('PGDATABASE'),
                user=os.environ.get('PGUSER'),
                password=os.environ.get('PGPASSWORD'),
                port=os.environ.get('PGPORT')
            )
            logging.info("PostgreSQL connection successful")
            conn.close()
        except Exception as e:
            logging.error(f"Error connecting to PostgreSQL: {e}")
            return

        # Add default admin user
        try:
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(username='admin')
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                logging.info("Admin user created successfully")
            else:
                logging.info("Admin user already exists")

            # Verify admin user creation
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                logging.info(f"Admin user found in database: {admin_user.username}")
                logging.info(f"Admin user password hash: {admin_user.password_hash}")
            else:
                logging.error("Admin user not found in database after creation attempt")

            # Check if User table exists and print all users
            users = User.query.all()
            logging.info(f"All users in the database: {[user.username for user in users]}")

        except Exception as e:
            logging.error(f"Error during admin user creation or verification: {e}")
            db.session.rollback()

        logging.info("Sample data has been added to the database.")

if __name__ == '__main__':
    seed_data()
