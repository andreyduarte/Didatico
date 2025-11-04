from __future__ import annotations

from typing import Dict, Tuple


def render_context(slide, theme_name: str) -> Tuple[str, Dict]:
    layout = (slide.layout or "hero").lower()
    blocks = slide.blocks or []

    def get_text(index: int = 0, default: str = ""):
        text_blocks = [b for b in blocks if b.type == "text"]
        if index < len(text_blocks):
            return (text_blocks[index].payload or {}).get("text", default)
        return default

    def get_image():
        for b in blocks:
            if b.type == "image":
                return (b.payload or {}).get("url")
        return None

    # Layouts comuns
    if layout == "hero":
        ctx = {"title": get_text(0, "Título do slide"), "image": get_image()}
        return f"themes/{theme_name}/hero.html", ctx

    if layout == "split":
        ctx = {"title": get_text(0, "Título"), "text": get_text(1, "Conteúdo"), "image": get_image()}
        return f"themes/{theme_name}/split.html", ctx

    if layout == "two_cols":
        ctx = {"text": get_text(0, "Conteúdo"), "image": get_image()}
        return f"themes/{theme_name}/two_cols.html", ctx

    if layout == "gallery":
        images = [(b.payload or {}).get("url") for b in blocks if b.type == "image"]
        ctx = {"images": [u for u in images if u]}
        return f"themes/{theme_name}/gallery.html", ctx

    if layout == "quote":
        ctx = {"quote": get_text(0, "Citação")}
        return f"themes/{theme_name}/quote.html", ctx

    # Layouts do tema academic
    if layout == "cover":
        ctx = {"title": get_text(0, "Título"), "text": get_text(1, "Subtítulo")}
        return f"themes/{theme_name}/cover.html", ctx

    if layout == "objective":
        ctx = {"title": get_text(0, "Objetivo"), "text": get_text(1, "Descrição")}
        return f"themes/{theme_name}/objective.html", ctx

    if layout == "statement":
        ctx = {"text": get_text(0, "Declaração")}
        return f"themes/{theme_name}/statement.html", ctx

    if layout == "quote_block":
        ctx = {"quote": get_text(0, "Citação"), "author": get_text(1, "")}
        return f"themes/{theme_name}/quote_block.html", ctx

    if layout == "section_break":
        ctx = {"title": get_text(0, "Seção")}
        return f"themes/{theme_name}/section_break.html", ctx

    if layout == "sidebar_summary":
        ctx = {"title": get_text(0, "Título"), "text": get_text(1, "Conteúdo"), "summary": get_text(2, "Resumo")}
        return f"themes/{theme_name}/sidebar_summary.html", ctx

    if layout == "reading_list":
        ctx = {"title": get_text(0, "Leituras"), "text": get_text(1, "Lista")}
        return f"themes/{theme_name}/reading_list.html", ctx

    # fallback
    return f"themes/{theme_name}/hero.html", {"title": get_text(0, "Slide"), "image": get_image()}
