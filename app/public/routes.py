from __future__ import annotations

from flask import Blueprint, abort, render_template

from ..models import Lesson

bp = Blueprint("public", __name__, url_prefix="/c")


@bp.route("/<slug>")
def view_lesson(slug: str):
    lesson = Lesson.query.filter_by(slug=slug, published=True).first()
    if not lesson:
        abort(404)
    return render_template("public/lesson.html", lesson=lesson)


