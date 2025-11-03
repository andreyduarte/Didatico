from __future__ import annotations

from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
from flask_wtf import FlaskForm


class LessonForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(max=200)])
    slug = StringField(
        "Slug",
        validators=[
            DataRequired(),
            Length(max=200),
            Regexp(r"^[a-z0-9-]+$", message="Use apenas letras minúsculas, números e hífens"),
        ],
    )
    description = TextAreaField("Descrição")
    submit = SubmitField("Salvar")


class BlockForm(FlaskForm):
    type = StringField("Tipo", validators=[DataRequired()])
    text = TextAreaField("Texto")
    image_url = StringField("URL da imagem")
    embed_url = StringField("URL do vídeo/embutido")
    list_items = TextAreaField("Lista (1 item por linha)")
    submit = SubmitField("Salvar")


