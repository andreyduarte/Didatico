THEME_LAYOUTS = {
    "default": [
        {"value": "hero", "label": "Hero"},
        {"value": "two_cols", "label": "Duas Colunas"},
        {"value": "split", "label": "Split (Título + Texto)"},
        {"value": "gallery", "label": "Galeria"},
        {"value": "quote", "label": "Citação"},
    ],
    "behaviorist": [
        {"value": "hero", "label": "Hero"},
        {"value": "two_cols", "label": "Duas Colunas"},
        {"value": "split", "label": "Split"},
        {"value": "quote", "label": "Citação"},
        {"value": "gallery", "label": "Galeria"},
    ],
    "academic": [
        {"value": "cover", "label": "Capa"},
        {"value": "objective", "label": "Objetivo"},
        {"value": "statement", "label": "Declaração"},
        {"value": "quote_block", "label": "Citação"},
        {"value": "section_break", "label": "Quebra de Seção"},
        {"value": "sidebar_summary", "label": "Resumo Lateral"},
        {"value": "reading_list", "label": "Lista de Leitura"},
    ],
}

LAYOUT_BLOCKS = {
    "hero": [{"type": "text", "payload": {"text": "Título do slide"}}],
    "two_cols": [{"type": "text", "payload": {"text": "Conteúdo"}}],
    "split": [{"type": "text", "payload": {"text": "Título"}}, {"type": "text", "payload": {"text": "Conteúdo"}}],
    "gallery": [],
    "quote": [{"type": "text", "payload": {"text": "Citação"}}],
    "cover": [{"type": "text", "payload": {"text": "Título"}}, {"type": "text", "payload": {"text": "Subtítulo"}}],
    "objective": [{"type": "text", "payload": {"text": "Objetivo"}}, {"type": "text", "payload": {"text": "Descrição"}}],
    "statement": [{"type": "text", "payload": {"text": "Declaração"}}],
    "quote_block": [{"type": "text", "payload": {"text": "Citação"}}, {"type": "text", "payload": {"text": "Autor"}}],
    "section_break": [{"type": "text", "payload": {"text": "Seção"}}],
    "sidebar_summary": [{"type": "text", "payload": {"text": "Título"}}, {"type": "text", "payload": {"text": "Conteúdo"}}, {"type": "text", "payload": {"text": "Resumo"}}],
    "reading_list": [{"type": "text", "payload": {"text": "Leituras"}}, {"type": "text", "payload": {"text": "Lista"}}],
}

def get_theme_layouts(theme_name):
    return THEME_LAYOUTS.get(theme_name, THEME_LAYOUTS["default"])

def get_layout_default_blocks(layout_name):
    return LAYOUT_BLOCKS.get(layout_name, [])
