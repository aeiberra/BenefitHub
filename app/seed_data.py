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
            logging.info("Checking for existing admin user...")
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                logging.info("Admin user not found. Creating new admin user...")
                admin_user = User(username='admin')
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                logging.info("Admin user created successfully")
            else:
                logging.info("Admin user already exists")

            # Add default categories if they don't exist
            categories = [
                {"name": "Educación", "image_url": "https://placehold.co/400x300?text=Educacion"},
                {"name": "Belleza", "image_url": "https://placehold.co/400x300?text=Belleza"},
                {"name": "Comida", "image_url": "https://placehold.co/400x300?text=Comida"},
                {"name": "Deportes", "image_url": "https://placehold.co/400x300?text=Deportes"},
                {"name": "Salud", "image_url": "https://placehold.co/400x300?text=Salud"},
                {"name": "Entretenimiento", "image_url": "https://placehold.co/400x300?text=Entretenimiento"},
                {"name": "Viajes", "image_url": "https://placehold.co/400x300?text=Viajes"},
                {"name": "Mascotas", "image_url": "https://placehold.co/400x300?text=Mascotas"}
            ]

            for category_data in categories:
                existing_category = Category.query.filter_by(name=category_data["name"]).first()
                if not existing_category:
                    new_category = Category(name=category_data["name"], image_url=category_data["image_url"])
                    db.session.add(new_category)
                    logging.info(f"Added new category: {category_data['name']}")
                else:
                    logging.info(f"Category already exists: {category_data['name']}")

            db.session.commit()
            logging.info("Categories added successfully")

        except Exception as e:
            logging.error(f"Error during data seeding: {e}")
            db.session.rollback()

        logging.info("Seed data process completed.")

if __name__ == '__main__':
    seed_data()
