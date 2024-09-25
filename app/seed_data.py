import os
from app import db, create_app
from app.models import Category, Benefit, User
import psycopg2

def seed_data():
    app = create_app()
    with app.app_context():
        # Test PostgreSQL connection
        try:
            conn = psycopg2.connect(
                host=os.environ.get('PGHOST'),
                database=os.environ.get('PGDATABASE'),
                user=os.environ.get('PGUSER'),
                password=os.environ.get('PGPASSWORD'),
                port=os.environ.get('PGPORT')
            )
            print("PostgreSQL connection successful")
            conn.close()
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return

        # Add categories
        categories = [
            {'name': 'Educación', 'image_url': 'https://placehold.co/400x300?text=Educacion'},
            {'name': 'Belleza', 'image_url': 'https://placehold.co/400x300?text=Belleza'},
            {'name': 'Comida', 'image_url': 'https://placehold.co/400x300?text=Comida'},
            {'name': 'Deportes', 'image_url': 'https://placehold.co/400x300?text=Deportes'},
            {'name': 'Salud', 'image_url': 'https://placehold.co/400x300?text=Salud'},
            {'name': 'Entretenimiento', 'image_url': 'https://placehold.co/400x300?text=Entretenimiento'},
            {'name': 'Viajes', 'image_url': 'https://placehold.co/400x300?text=Viajes'},
            {'name': 'Mascotas', 'image_url': 'https://placehold.co/400x300?text=Mascotas'}
        ]

        for category_data in categories:
            category = Category.query.filter_by(name=category_data['name']).first()
            if not category:
                category = Category(**category_data)
                db.session.add(category)
        
        db.session.commit()

        # Add benefits
        benefits = [
            {'name': 'Curso de inglés online', 'description': '50% de descuento en curso de inglés online', 'image_url': 'https://placehold.co/400x300?text=Curso+de+ingles', 'company': 'Language Academy', 'category_name': 'Educación'},
            {'name': 'Spa day', 'description': '20% de descuento en día de spa', 'image_url': 'https://placehold.co/400x300?text=Spa+day', 'company': 'Relax Spa', 'category_name': 'Belleza'},
            {'name': 'Pizza 2x1', 'description': 'Compra una pizza y llévate otra gratis', 'image_url': 'https://placehold.co/400x300?text=Pizza+2x1', 'company': 'Pizza Heaven', 'category_name': 'Comida'},
            {'name': 'Gimnasio mensualidad', 'description': '30% de descuento en membresía mensual', 'image_url': 'https://placehold.co/400x300?text=Gimnasio', 'company': 'FitLife Gym', 'category_name': 'Deportes'},
            {'name': 'Consulta médica', 'description': 'Consulta médica general gratuita', 'image_url': 'https://placehold.co/400x300?text=Consulta+medica', 'company': 'HealthCare Center', 'category_name': 'Salud'},
            {'name': 'Entradas al cine', 'description': '2x1 en entradas al cine', 'image_url': 'https://placehold.co/400x300?text=Cine', 'company': 'CineStar', 'category_name': 'Entretenimiento'},
            {'name': 'Descuento en hotel', 'description': '15% de descuento en reserva de hotel', 'image_url': 'https://placehold.co/400x300?text=Hotel', 'company': 'Comfort Inn', 'category_name': 'Viajes'},
            {'name': 'Alimento para mascotas', 'description': '10% de descuento en alimento para mascotas', 'image_url': 'https://placehold.co/400x300?text=Alimento+mascotas', 'company': 'Pet Paradise', 'category_name': 'Mascotas'}
        ]

        for benefit_data in benefits:
            category = Category.query.filter_by(name=benefit_data['category_name']).first()
            if category:
                benefit = Benefit.query.filter_by(name=benefit_data['name'], category_id=category.id).first()
                if not benefit:
                    benefit = Benefit(
                        name=benefit_data['name'],
                        description=benefit_data['description'],
                        image_url=benefit_data['image_url'],
                        company=benefit_data['company'],
                        category_id=category.id
                    )
                    db.session.add(benefit)
        
        db.session.commit()

        # Add default admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()

    print("Sample data has been added to the database.")

if __name__ == '__main__':
    seed_data()
