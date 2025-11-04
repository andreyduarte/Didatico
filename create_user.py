from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    u = User(email="admin@example.com")
    u.set_password("admin123")
    db.session.add(u)
    db.session.commit()
    print("Usuário criado com sucesso!")
    print("Email: admin@example.com")
    print("Senha: admin123")
