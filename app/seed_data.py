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

        # Add categories and benefits (existing code)
        # ...

        # Add default admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            try:
                db.session.commit()
                logging.info("Admin user created successfully")
            except Exception as e:
                db.session.rollback()
                logging.error(f"Error creating admin user: {e}")
        else:
            logging.info("Admin user already exists")

        # Verify admin user creation
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            logging.info(f"Admin user found in database: {admin_user.username}")
        else:
            logging.error("Admin user not found in database after creation attempt")

    logging.info("Sample data has been added to the database.")

if __name__ == '__main__':
    seed_data()
