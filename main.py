from app import create_app, db
from app.models import User, Category, Benefit, Redemption
from app.seed_data import seed_data
from flask_migrate import Migrate, upgrade, init, migrate
import os
import logging

app = create_app()
migrate = Migrate(app, db)

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
        # Initialize migration repository if it doesn't exist
        if not os.path.exists('migrations'):
            init()
            logging.info("Migration repository initialized")

        # Create a new migration
        migrate()
        logging.info("New migration created")

        # Apply the migration
        upgrade()
        logging.info("Database migration completed successfully")

        # Run seed_data to create admin user and add default data if needed
        logging.info("Running seed_data function...")
        seed_data()

        # Verify admin user after seeding
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            logging.info(f"Admin user verified - Username: {admin_user.username}, ID: {admin_user.id}")
        else:
            logging.warning("Admin user not found in the database after seeding")

        # Print all users in the database
        users = User.query.all()
        logging.info("Users in the database:")
        for user in users:
            logging.info(f"Username: {user.username}, ID: {user.id}")

    except Exception as e:
        logging.error(f"Error occurred during database setup or seeding: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
