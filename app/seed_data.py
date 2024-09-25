from app import db, create_app
from app.models import Category, Benefit

def seed_data():
    app = create_app()
    with app.app_context():
        # Add categories
        categories = [
            Category(name='Educación'),
            Category(name='Belleza'),
            Category(name='Comida'),
            Category(name='Deportes'),
            Category(name='Salud'),
            Category(name='Entretenimiento'),
            Category(name='Viajes'),
            Category(name='Mascotas')
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Add benefits
        benefits = [
            Benefit(name='Curso de inglés online', description='50% de descuento en curso de inglés online', image_url='https://placehold.co/400x300?text=Curso+de+ingles', company='Language Academy', category_id=1),
            Benefit(name='Spa day', description='20% de descuento en día de spa', image_url='https://placehold.co/400x300?text=Spa+day', company='Relax Spa', category_id=2),
            Benefit(name='Pizza 2x1', description='Compra una pizza y llévate otra gratis', image_url='https://placehold.co/400x300?text=Pizza+2x1', company='Pizza Heaven', category_id=3),
            Benefit(name='Gimnasio mensualidad', description='30% de descuento en membresía mensual', image_url='https://placehold.co/400x300?text=Gimnasio', company='FitLife Gym', category_id=4),
            Benefit(name='Consulta médica', description='Consulta médica general gratuita', image_url='https://placehold.co/400x300?text=Consulta+medica', company='HealthCare Center', category_id=5),
            Benefit(name='Entradas al cine', description='2x1 en entradas al cine', image_url='https://placehold.co/400x300?text=Cine', company='CineStar', category_id=6),
            Benefit(name='Descuento en hotel', description='15% de descuento en reserva de hotel', image_url='https://placehold.co/400x300?text=Hotel', company='Comfort Inn', category_id=7),
            Benefit(name='Alimento para mascotas', description='10% de descuento en alimento para mascotas', image_url='https://placehold.co/400x300?text=Alimento+mascotas', company='Pet Paradise', category_id=8)
        ]
        db.session.add_all(benefits)
        db.session.commit()

if __name__ == '__main__':
    seed_data()
    print("Sample data has been added to the database.")
