THEME_LAYOUTS = {
    "default": [
        {"value": "titulo", "label": "Título"},
        {"value": "conteudo", "label": "Conteúdo"},
        {"value": "sumario", "label": "Sumário"},
        {"value": "subtitulo", "label": "Subtítulo"},
    ],
}

LAYOUT_BLOCKS = {
    "titulo": [
        {"type": "text", "payload": {"text": "Título"}},
        {"type": "text", "payload": {"text": "Subtítulo"}},
    ],
    "conteudo": [
        {"type": "text", "payload": {"text": "Conteúdo"}},
        {"type": "text", "payload": {"text": "Rodapé"}},
    ],
    "sumario": [
        {"type": "text", "payload": {"text": "Título"}},
        {"type": "text", "payload": {"text": "Parágrafo"}},
        {"type": "text", "payload": {"text": "Conteúdo principal"}},
    ],
    "subtitulo": [
        {"type": "text", "payload": {"text": "Subtítulo"}},
    ],
}

def get_theme_layouts(theme_name):
    return THEME_LAYOUTS.get(theme_name, THEME_LAYOUTS["default"])

def get_layout_default_blocks(layout_name):
    return LAYOUT_BLOCKS.get(layout_name, [])
