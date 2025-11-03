from __future__ import annotations

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user

from .. import db
from ..models import Lesson, Slide, SlideBlock
from ..forms import LessonForm, BlockForm
from ..services.storage import save_image

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    lessons = Lesson.query.filter_by(user_id=current_user.id).order_by(Lesson.created_at.desc()).all()
    return render_template("dashboard/index.html", lessons=lessons)


@bp.route("/lesson/new", methods=["GET", "POST"])
@login_required
def lesson_new():
    form = LessonForm()
    if form.validate_on_submit():
        # Checa slug único por usuário
        exists = (
            Lesson.query.filter_by(user_id=current_user.id, slug=form.slug.data).first()
            is not None
        )
        if exists:
            flash("Slug já usado nesta conta.", "danger")
        else:
            lesson = Lesson(
                user_id=current_user.id,
                title=form.title.data.strip(),
                slug=form.slug.data.strip(),
                description=form.description.data or "",
            )
            db.session.add(lesson)
            db.session.commit()
            flash("Aula criada.", "success")
            return redirect(url_for("dashboard.index"))
    return render_template("dashboard/lesson_form.html", form=form, is_edit=False)


@bp.route("/lesson/<int:lesson_id>/edit", methods=["GET", "POST"])
@login_required
def lesson_edit(lesson_id: int):
    lesson = Lesson.query.filter_by(id=lesson_id, user_id=current_user.id).first_or_404()
    form = LessonForm(obj=lesson)
    if form.validate_on_submit():
        # Valida slug se alterado
        if form.slug.data != lesson.slug:
            exists = (
                Lesson.query.filter_by(user_id=current_user.id, slug=form.slug.data).first()
                is not None
            )
            if exists:
                flash("Slug já usado nesta conta.", "danger")
                return render_template("dashboard/lesson_form.html", form=form, is_edit=True)
        lesson.title = form.title.data.strip()
        lesson.slug = form.slug.data.strip()
        lesson.description = form.description.data or ""
        db.session.commit()
        flash("Aula atualizada.", "success")
        return redirect(url_for("dashboard.index"))
    return render_template("dashboard/lesson_form.html", form=form, is_edit=True)


@bp.route("/lesson/<int:lesson_id>/publish", methods=["POST"])
@login_required
def lesson_publish(lesson_id: int):
    lesson = Lesson.query.filter_by(id=lesson_id, user_id=current_user.id).first_or_404()
    action = request.form.get("action", "toggle")
    if action == "publish":
        lesson.published = True
    elif action == "unpublish":
        lesson.published = False
    else:
        lesson.published = not lesson.published
    db.session.commit()
    state = "publicada" if lesson.published else "como rascunho"
    flash(f"Aula marcada {state}.", "success")
    return redirect(url_for("dashboard.index"))


@bp.route("/lesson/<int:lesson_id>/slides")
@login_required
def slides_manage(lesson_id: int):
    lesson = Lesson.query.filter_by(id=lesson_id, user_id=current_user.id).first_or_404()
    slides = Slide.query.filter_by(lesson_id=lesson.id).order_by(Slide.order).all()
    return render_template("dashboard/slides.html", lesson=lesson, slides=slides)


@bp.route("/lesson/<int:lesson_id>/slide/new", methods=["POST"])
@login_required
def slide_new(lesson_id: int):
    lesson = Lesson.query.filter_by(id=lesson_id, user_id=current_user.id).first_or_404()
    max_order = db.session.query(db.func.max(Slide.order)).filter_by(lesson_id=lesson.id).scalar()
    next_order = (max_order or 0) + 1
    slide = Slide(lesson_id=lesson.id, order=next_order, layout="hero")
    db.session.add(slide)
    db.session.commit()
    flash("Slide criado.", "success")
    return redirect(url_for("dashboard.slides_manage", lesson_id=lesson.id))


@bp.route("/slide/<int:slide_id>/delete", methods=["POST"])
@login_required
def slide_delete(slide_id: int):
    slide = (
        db.session.query(Slide)
        .join(Lesson, Slide.lesson_id == Lesson.id)
        .filter(Slide.id == slide_id, Lesson.user_id == current_user.id)
        .first_or_404()
    )
    lesson_id = slide.lesson_id
    db.session.delete(slide)
    db.session.commit()
    flash("Slide removido.", "success")
    return redirect(url_for("dashboard.slides_manage", lesson_id=lesson_id))


@bp.route("/slide/<int:slide_id>/move", methods=["POST"])
@login_required
def slide_move(slide_id: int):
    direction = request.form.get("direction")
    slide = (
        db.session.query(Slide)
        .join(Lesson, Slide.lesson_id == Lesson.id)
        .filter(Slide.id == slide_id, Lesson.user_id == current_user.id)
        .first_or_404()
    )
    if direction == "up":
        prev = (
            Slide.query.filter(Slide.lesson_id == slide.lesson_id, Slide.order < slide.order)
            .order_by(Slide.order.desc())
            .first()
        )
        if prev:
            prev.order, slide.order = slide.order, prev.order
    elif direction == "down":
        nxt = (
            Slide.query.filter(Slide.lesson_id == slide.lesson_id, Slide.order > slide.order)
            .order_by(Slide.order.asc())
            .first()
        )
        if nxt:
            nxt.order, slide.order = slide.order, nxt.order
    db.session.commit()
    return redirect(url_for("dashboard.slides_manage", lesson_id=slide.lesson_id))


@bp.route("/slide/<int:slide_id>/blocks")
@login_required
def blocks_manage(slide_id: int):
    slide = (
        db.session.query(Slide)
        .join(Lesson, Slide.lesson_id == Lesson.id)
        .filter(Slide.id == slide_id, Lesson.user_id == current_user.id)
        .first_or_404()
    )
    blocks = SlideBlock.query.filter_by(slide_id=slide.id).order_by(SlideBlock.order).all()
    return render_template("dashboard/blocks.html", slide=slide, blocks=blocks)


@bp.route("/slide/<int:slide_id>/block/new", methods=["GET", "POST"])
@login_required
def block_new(slide_id: int):
    slide = (
        db.session.query(Slide)
        .join(Lesson, Slide.lesson_id == Lesson.id)
        .filter(Slide.id == slide_id, Lesson.user_id == current_user.id)
        .first_or_404()
    )
    form = BlockForm()
    if form.validate_on_submit():
        max_order = db.session.query(db.func.max(SlideBlock.order)).filter_by(slide_id=slide.id).scalar()
        next_order = (max_order or 0) + 1
        payload = {}
        if form.type.data == "text":
            payload = {"text": form.text.data or ""}
        elif form.type.data == "image":
            payload = {"url": form.image_url.data or ""}
        elif form.type.data == "embed":
            payload = {"url": form.embed_url.data or ""}
        elif form.type.data == "list":
            items = [line.strip() for line in (form.list_items.data or "").splitlines() if line.strip()]
            payload = {"items": items}
        block = SlideBlock(slide_id=slide.id, type=form.type.data, payload=payload, order=next_order)
        db.session.add(block)
        db.session.commit()
        flash("Bloco adicionado.", "success")
        return redirect(url_for("dashboard.blocks_manage", slide_id=slide.id))
    return render_template("dashboard/block_form.html", form=form, is_edit=False, slide=slide)


@bp.route("/block/<int:block_id>/edit", methods=["GET", "POST"])
@login_required
def block_edit(block_id: int):
    block = (
        db.session.query(SlideBlock)
        .join(Slide, SlideBlock.slide_id == Slide.id)
        .join(Lesson, Slide.lesson_id == Lesson.id)
        .filter(SlideBlock.id == block_id, Lesson.user_id == current_user.id)
        .first_or_404()
    )
    form = BlockForm(
        type=block.type,
        text=(block.payload or {}).get("text"),
        image_url=(block.payload or {}).get("url"),
        embed_url=(block.payload or {}).get("url"),
        list_items="\n".join((block.payload or {}).get("items", [])),
    )
    if form.validate_on_submit():
        if form.type.data != block.type:
            flash("Tipo não pode ser alterado neste MVP.", "warning")
        else:
            if block.type == "text":
                block.payload = {"text": form.text.data or ""}
            elif block.type == "image":
                block.payload = {"url": form.image_url.data or ""}
            elif block.type == "embed":
                block.payload = {"url": form.embed_url.data or ""}
            elif block.type == "list":
                items = [line.strip() for line in (form.list_items.data or "").splitlines() if line.strip()]
                block.payload = {"items": items}
            db.session.commit()
            flash("Bloco atualizado.", "success")
            return redirect(url_for("dashboard.blocks_manage", slide_id=block.slide_id))
    return render_template("dashboard/block_form.html", form=form, is_edit=True, slide=block.slide)


@bp.route("/block/<int:block_id>/delete", methods=["POST"])
@login_required
def block_delete(block_id: int):
    block = (
        db.session.query(SlideBlock)
        .join(Slide, SlideBlock.slide_id == Slide.id)
        .join(Lesson, Slide.lesson_id == Lesson.id)
        .filter(SlideBlock.id == block_id, Lesson.user_id == current_user.id)
        .first_or_404()
    )
    slide_id = block.slide_id
    db.session.delete(block)
    db.session.commit()
    flash("Bloco removido.", "success")
    return redirect(url_for("dashboard.blocks_manage", slide_id=slide_id))


@bp.route("/block/<int:block_id>/move", methods=["POST"])
@login_required
def block_move(block_id: int):
    direction = request.form.get("direction")
    block = (
        db.session.query(SlideBlock)
        .join(Slide, SlideBlock.slide_id == Slide.id)
        .join(Lesson, Slide.lesson_id == Lesson.id)
        .filter(SlideBlock.id == block_id, Lesson.user_id == current_user.id)
        .first_or_404()
    )
    if direction == "up":
        prev = (
            SlideBlock.query.filter(SlideBlock.slide_id == block.slide_id, SlideBlock.order < block.order)
            .order_by(SlideBlock.order.desc())
            .first()
        )
        if prev:
            prev.order, block.order = block.order, prev.order
    elif direction == "down":
        nxt = (
            SlideBlock.query.filter(SlideBlock.slide_id == block.slide_id, SlideBlock.order > block.order)
            .order_by(SlideBlock.order.asc())
            .first()
        )
        if nxt:
            nxt.order, block.order = block.order, nxt.order
    db.session.commit()
    return redirect(url_for("dashboard.blocks_manage", slide_id=block.slide_id))


@bp.route("/slide/<int:slide_id>/upload", methods=["POST"])
@login_required
def upload_image(slide_id: int):
    slide = (
        db.session.query(Slide)
        .join(Lesson, Slide.lesson_id == Lesson.id)
        .filter(Slide.id == slide_id, Lesson.user_id == current_user.id)
        .first_or_404()
    )
    file = request.files.get("file")
    if not file:
        flash("Arquivo não enviado.", "danger")
        return redirect(url_for("dashboard.blocks_manage", slide_id=slide.id))
    try:
        url, _ = save_image(file, upload_root=current_app.config["UPLOAD_FOLDER"])
        return redirect(url_for("dashboard.blocks_manage", slide_id=slide.id, uploaded=url))
    except Exception as e:  # pragma: no cover
        flash(str(e), "danger")
        return redirect(url_for("dashboard.blocks_manage", slide_id=slide.id))




