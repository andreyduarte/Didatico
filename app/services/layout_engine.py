from __future__ import annotations

from typing import Dict, Tuple


def render_context(slide, theme_name: str) -> Tuple[str, Dict]:
    layout = (slide.layout or "titulo").lower()
    blocks = slide.blocks or []

    def get_text(index: int = 0, default: str = "") -> str:
        text_blocks = [b for b in blocks if b.type == "text"]
        if index < len(text_blocks):
            return (text_blocks[index].payload or {}).get("text", default)
        return default

    def get_image():
        for b in blocks:
            if b.type == "image":
                return (b.payload or {}).get("url")
        return None

    # Título
    if layout == "titulo":
        ctx = {
            "title": get_text(0, "Título"),
            "subtitle": get_text(1, "Subtítulo"),
            "bg_color": getattr(slide, 'background', None) or "#6366f1"
        }
        return f"themes/{theme_name}/titulo.html", ctx

    # Conteúdo
    if layout == "conteudo":
        ctx = {
            "text": get_text(0, "Conteúdo"),
            "footer": get_text(1, "Rodapé"),
            "image": get_image(),
            "bg_color": getattr(slide, 'background', None) or "#6366f1"
        }
        return f"themes/{theme_name}/conteudo.html", ctx

    # Sumário
    if layout == "sumario":
        ctx = {
            "title": get_text(0, "Título"),
            "paragraph": get_text(1, "Parágrafo"),
            "content": get_text(2, "Conteúdo principal"),
            "image": get_image(),
            "bg_color": getattr(slide, 'background', None) or "#6366f1"
        }
        return f"themes/{theme_name}/sumario.html", ctx

    # Subtítulo
    if layout == "subtitulo":
        ctx = {
            "subtitle": get_text(0, "Subtítulo"),
            "bg_color": getattr(slide, 'background', None) or "#6366f1"
        }
        return f"themes/{theme_name}/subtitulo.html", ctx

    # Fallback
    return f"themes/{theme_name}/titulo.html", {
        "title": get_text(0, "Slide"),
        "subtitle": "",
        "bg_color": "#6366f1"
    }
