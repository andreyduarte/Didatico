from __future__ import annotations

from typing import Dict, Tuple


def render_context(slide, theme_name: str) -> Tuple[str, Dict]:
    layout = (slide.layout or "titulo").lower()
    blocks = slide.blocks or []
    text_blocks = [b for b in blocks if b.type == "text"]
    image_blocks = [b for b in blocks if b.type == "image"]

    def get_text(index: int = 0, default: str = "") -> str:
        if index < len(text_blocks):
            return (text_blocks[index].payload or {}).get("text", default)
        return default
    
    def get_text_block_id(index: int = 0):
        if index < len(text_blocks):
            return text_blocks[index].id
        return None

    def get_image():
        if image_blocks:
            return (image_blocks[0].payload or {}).get("url")
        return None
    
    def get_image_block_id():
        if image_blocks:
            return image_blocks[0].id
        return None

    # Título
    if layout == "titulo":
        ctx = {
            "title": get_text(0, "Título"),
            "subtitle": get_text(1, "Subtítulo"),
            "title_block_id": get_text_block_id(0),
            "subtitle_block_id": get_text_block_id(1),
            "bg_color": getattr(slide, 'background', None) or "#6366f1"
        }
        return f"themes/{theme_name}/titulo.html", ctx

    # Conteúdo
    if layout == "conteudo":
        ctx = {
            "text": get_text(0, "Conteúdo"),
            "footer": get_text(1, "Rodapé"),
            "image": get_image(),
            "text_block_id": get_text_block_id(0),
            "footer_block_id": get_text_block_id(1),
            "image_block_id": get_image_block_id(),
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
            "title_block_id": get_text_block_id(0),
            "paragraph_block_id": get_text_block_id(1),
            "content_block_id": get_text_block_id(2),
            "image_block_id": get_image_block_id(),
            "bg_color": getattr(slide, 'background', None) or "#6366f1"
        }
        return f"themes/{theme_name}/sumario.html", ctx

    # Subtítulo
    if layout == "subtitulo":
        ctx = {
            "subtitle": get_text(0, "Subtítulo"),
            "subtitle_block_id": get_text_block_id(0),
            "bg_color": getattr(slide, 'background', None) or "#6366f1"
        }
        return f"themes/{theme_name}/subtitulo.html", ctx

    # Fallback
    return f"themes/{theme_name}/titulo.html", {
        "title": get_text(0, "Slide"),
        "subtitle": "",
        "bg_color": "#6366f1"
    }
