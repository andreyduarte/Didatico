# Aulas dinâmicas (MVP Flask)

## Setup rápido

1. Crie e ative um ambiente virtual
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicie app e banco:
   ```bash
   set FLASK_APP=app
   flask --app app init-db
   flask --app app run --debug
   ```

- Banco: `instance/app.db`
- Uploads locais: `instance/uploads/`

## Login inicial

Crie um usuário via shell Python:
```python
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    u = User(email="prof@example.com")
    u.set_password("senha123")
    db.session.add(u)
    db.session.commit()
```
Acesse `/auth/login` e entre.

## Estrutura
- Blueprints: `auth`, `dashboard`, `public`
- Modelos: `User`, `Lesson`, `Slide`, `SlideBlock`

## Fluxo no dashboard (MVP)
- Criar aula: Dashboard → Nova aula
- Gerenciar slides: Dashboard → Editar → Slides
- Gerenciar blocos: Slides → Blocos
- Upload de imagem: na página de Blocos (copia a URL gerada)

## Visualização pública
- Link: `/c/<slug>`
- Suporta layouts: `hero`, `two_cols`, `gallery`, `quote`

## Testes
```bash
pytest -q
```

> Este é apenas o esqueleto do MVP. Próximos passos: modelos completos, auth, CRUDs e engine de layout.


