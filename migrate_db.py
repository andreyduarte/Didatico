"""Script para adicionar coluna content_html na tabela slide"""
from app import create_app, db

app = create_app()

with app.app_context():
    try:
        # Tenta adicionar a coluna
        with db.engine.connect() as conn:
            conn.execute(db.text("ALTER TABLE slide ADD COLUMN content_html TEXT DEFAULT ''"))
            conn.commit()
            print("[OK] Coluna content_html adicionada com sucesso!")
    except Exception as e:
        if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
            print("[OK] Coluna content_html ja existe")
        else:
            print(f"[ERRO] {e}")
            print("\nTente uma das alternativas:")
            print("1. Deletar e recriar o banco:")
            print("   del instance\\app.db")
            print("   flask --app app init-db")
            print("\n2. Ou adicionar manualmente via SQLite:")
            print("   sqlite3 instance\\app.db")
            print("   ALTER TABLE slide ADD COLUMN content_html TEXT DEFAULT '';")
