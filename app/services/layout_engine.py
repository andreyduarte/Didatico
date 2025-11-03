from __future__ import annotations

from typing import Dict, Tuple


def render_context(slide, theme_name: str) -> Tuple[str, Dict]:
    layout = (slide.layout or "hero").lower()
    blocks = slide.blocks or []

    def get_text(default: str = ""):
        for b in blocks:
            if b.type == "text":
                return (b.payload or {}).get("text", default)
        return default

    def get_image():
        for b in blocks:
            if b.type == "image":
                return (b.payload or {}).get("url")
        return None

    if layout == "hero":
        ctx = {
            "title": get_text("Título do slide"),
            "image": get_image(),
        }
        return f"themes/{theme_name}/hero.html", ctx

    if layout == "split":
        ctx = {
            "title": get_text("Título do slide"),
            "text": get_text("Conteúdo"),
            "image": get_image(),
        }
        return f"themes/{theme_name}/split.html", ctx

    if layout == "two_cols":
        # primeira imagem + primeiro texto
        ctx = {
            "text": get_text("Conteúdo"),
            "image": get_image(),
        }
        return f"themes/{theme_name}/two_cols.html", ctx

    if layout == "gallery":
        images = [(b.payload or {}).get("url") for b in blocks if b.type == "image"]
        ctx = {"images": [u for u in images if u]}
        return f"themes/{theme_name}/gallery.html", ctx

    if layout == "quote":
        ctx = {"quote": get_text("Citação")}
        return f"themes/{theme_name}/quote.html", ctx

    # fallback
    return f"themes/{theme_name}/hero.html", {"title": get_text("Slide"), "image": get_image()}
