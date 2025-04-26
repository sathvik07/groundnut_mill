from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin = User(
            email='admin@example.com',
            username='admin'
        )
        admin.password = 'admin123'  # ✅ triggers password hashing
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
