from __future__ import annotations

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    lessons = db.relationship("Lesson", backref="owner", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id: str):  # pragma: no cover
    return User.query.get(int(user_id))


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    theme = db.Column(db.String(50), default="default")
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    slides = db.relationship(
        "Slide", backref="lesson", lazy=True, order_by="Slide.order"
    )

    __table_args__ = (db.UniqueConstraint("user_id", "slug", name="uix_user_slug"),)


class Slide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=False)
    order = db.Column(db.Integer, default=0)
    layout = db.Column(db.String(50), nullable=False, default="hero")
    background = db.Column(db.String(255), nullable=True)
    content_html = db.Column(db.Text, default="")

    blocks = db.relationship(
        "SlideBlock", backref="slide", lazy=True, order_by="SlideBlock.order"
    )


class SlideBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slide_id = db.Column(db.Integer, db.ForeignKey("slide.id"), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    payload = db.Column(db.JSON, nullable=False, default={})
    order = db.Column(db.Integer, default=0)


