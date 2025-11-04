from __future__ import annotations

import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate # Importar Flask-Migrate

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate() # Inicializar Migrate


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # Configurações básicas
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        secret_key = "dev-secret-key-change"

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            f"sqlite:///{Path(app.instance_path) / 'app.db'}",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=str(Path(app.instance_path) / "uploads"),
        MAX_CONTENT_LENGTH=20 * 1024 * 1024,  # 20MB
    )

    # Garante diretórios em instance/
    try:
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
        Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

    # Extensões
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db) # Inicializar Flask-Migrate com o app e o db

    login_manager.login_view = "auth.login"

    # Blueprints
    from .auth.routes import bp as auth_bp
    from .dashboard.routes import bp as dashboard_bp
    from .public.routes import bp as public_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(public_bp)

    # Servir uploads locais com segurança básica
    from flask import send_from_directory, abort, render_template
    from markupsafe import Markup
    from .services import layout_engine

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename: str):  # pragma: no cover
        upload_dir = Path(app.config["UPLOAD_FOLDER"]) 
        path = upload_dir / filename
        # Impede path traversal
        try:
            path.resolve().relative_to(upload_dir.resolve())
        except Exception:
            abort(404)
        if not path.exists():
            abort(404)
        return send_from_directory(upload_dir, filename)

    @app.context_processor
    def inject_render_slide():  # pragma: no cover
        def render_slide(slide, theme):
            theme_name = theme if isinstance(theme, str) else "default"
            tpl, ctx = layout_engine.render_context(slide, theme_name)
            html = render_template(tpl, **ctx)
            return Markup(html)

        return {"render_slide": render_slide}

    # CLI simples para criar DB
    @app.cli.command("init-db")
    def init_db_command():  # pragma: no cover
        from .models import User
        db.create_all()
        # Create a test user
        if not User.query.filter_by(email="testuser@example.com").first():
            user = User(email="testuser@example.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()
            print("Usuário de teste criado.")
        print("Banco inicializado em instance/app.db")

    return app
