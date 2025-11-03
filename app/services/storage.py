from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Tuple

from PIL import Image
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def is_allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file_storage, upload_root: str, max_width: int = 1600) -> Tuple[str, Path]:
    filename = secure_filename(file_storage.filename or "image")
    if not is_allowed(filename):
        raise ValueError("Extensão de arquivo não permitida")

    now = datetime.utcnow()
    subdir = Path(upload_root) / f"{now.year:04d}" / f"{now.month:02d}"
    subdir.mkdir(parents=True, exist_ok=True)

    # Gera nome único
    stem = Path(filename).stem
    ext = Path(filename).suffix.lower()
    path = subdir / f"{stem}{ext}"
    counter = 1
    while path.exists():
        path = subdir / f"{stem}_{counter}{ext}"
        counter += 1

    file_storage.save(path)

    # Valida que é imagem usando Pillow (compatível com Python 3.13+)
    try:
        with Image.open(path) as img_verify:
            img_verify.verify()
    except Exception:
        path.unlink(missing_ok=True)
        raise ValueError("Arquivo não é uma imagem válida")

    # Redimensiona se necessário
    try:
        img = Image.open(path)
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_size = (max_width, int(img.height * ratio))
            img = img.convert("RGB")
            img = img.resize(new_size, Image.LANCZOS)
            img.save(path)
    except Exception:
        # Em caso de falha, mantém arquivo original
        pass

    rel_url = f"/uploads/{now.year:04d}/{now.month:02d}/{path.name}"
    return rel_url, path


