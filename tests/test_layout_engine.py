from types import SimpleNamespace

from app.services.layout_engine import render_context


class Block(SimpleNamespace):
    pass


class Slide(SimpleNamespace):
    pass


def test_render_hero_uses_text_and_image():
    slide = Slide(layout="hero", blocks=[
        Block(type="text", payload={"text": "Titulo"}),
        Block(type="image", payload={"url": "/uploads/2025/10/img.jpg"}),
    ])
    tpl, ctx = render_context(slide)
    assert tpl.endswith("hero.html")
    assert ctx["title"] == "Titulo"
    assert ctx["image"].endswith("img.jpg")


