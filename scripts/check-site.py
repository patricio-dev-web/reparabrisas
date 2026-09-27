"""Validación local sin dependencias ni acceso de red."""
from collections import Counter
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
errors = []


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.links = []
        self.h1 = 0
        self.tags = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == "img" and ("alt" not in attrs or "width" not in attrs or "height" not in attrs):
            errors.append("Imagen sin texto alternativo o dimensiones: " + str(attrs))


docs = {}
for path in [ROOT / "index.html", *sorted((ROOT / "servicios").glob("*.html"))]:
    source = path.read_text(encoding="utf-8")
    document = Document(source)
    docs[path.resolve()] = document
    if document.h1 != 1:
        errors.append(f"{path.name}: debe tener exactamente un H1")
    if any(count > 1 for count in Counter(document.ids).values()):
        errors.append(f"{path.name}: IDs duplicados")
    if not any(tag == "meta" and attrs.get("name") == "description" and attrs.get("content") for tag, attrs in document.tags):
        errors.append(f"{path.name}: falta descripción")
    if not re.search(r'<title>.+?</title>', source):
        errors.append(f"{path.name}: falta título")
    for schema in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        json.loads(schema)
    for phone in re.findall(r'wa\.me/(\d+)|tel:(\+\d+)', source):
        if (phone[0] or phone[1].lstrip("+")) != "56976957866":
            errors.append(f"{path.name}: teléfono incorrecto")
    if not any(tag == "html" and attrs.get("lang") == "es-CL" for tag, attrs in document.tags):
        errors.append(f"{path.name}: falta idioma")

for path, document in docs.items():
    for link in document.links:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc:
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        if not target.is_file():
            errors.append(f"{path.name}: archivo inexistente {link}")
        if parts.fragment and target in docs and unquote(parts.fragment) not in docs[target].ids:
            errors.append(f"{path.name}: ancla inexistente {link}")

for path in [*docs, ROOT / "assets/css/style.css", ROOT / "assets/js/main.js"]:
    source = path.read_text(encoding="utf-8")
    if re.search(r'^(?:<{7}|={7}|>{7})', source, re.M):
        errors.append(f"{path.name}: conflicto sin resolver")
    if "\ufffd" in source:
        errors.append(f"{path.name}: error de codificación")

if not (ROOT / "assets/images/social-card.png").is_file():
    errors.append("Falta imagen social PNG")

# Comprobar generación, cambio de dominio y subcarpeta fuera del sitio real.
spec = importlib.util.spec_from_file_location("seo", ROOT / "scripts/configure-seo.py")
seo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seo)
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    for page in seo.PAGES:
        (root / page).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / page, root / page)
    base = "https://prueba-seo.example/reparabrisas"
    seo.configure(root, base)
    snapshot = [(root / page).read_text(encoding="utf-8") for page in seo.PAGES]
    seo.configure(root, base)
    assert snapshot == [(root / page).read_text(encoding="utf-8") for page in seo.PAGES], "Generador no idempotente"
    tree = ET.parse(root / "sitemap.xml")
    locations = [node.text for node in tree.findall('.//{*}loc')]
    assert locations == [base + "/", *[base + "/" + page for page in seo.PAGES[1:]]]
    assert (root / "robots.txt").read_text(encoding="utf-8").endswith(base + "/sitemap.xml\n")
    for page in seo.PAGES:
        html = (root / page).read_text(encoding="utf-8")
        assert html.count('rel="canonical"') == 1
        assert 'property="og:image"' in html
        for schema in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            assert json.loads(schema)["url"].startswith(base)
    for invalid in ("http://example.cl", "https://example.com", "https://localhost", "https://example.cl/?q=1"):
        try:
            seo.configure(root, invalid)
            raise AssertionError("Dominio inválido aceptado")
        except ValueError:
            pass
    seo.configure(root, "https://otro-dominio.example")
    assert base not in (root / "index.html").read_text(encoding="utf-8")

if errors:
    raise SystemExit("\n".join(errors))
print(f"OK: {len(docs)} páginas, enlaces, anclas, teléfono, metadatos, JSON-LD y generador SEO.")
