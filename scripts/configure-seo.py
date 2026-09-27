"""Genera URLs públicas sin asumir un dominio ni publicar archivos."""
import argparse
import html
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "servicios/reparacion-de-parabrisas.html", "servicios/grabado-de-patentes.html")


def configure(root, base_url):
    base_url = base_url.rstrip("/")
    parts = urlsplit(base_url)
    if (parts.scheme != "https" or not parts.hostname or parts.query or parts.fragment
            or parts.username or parts.password or any(c.isspace() for c in base_url)):
        raise ValueError("Usa una URL HTTPS pública, sin credenciales, consulta ni fragmento.")
    if parts.hostname in ("localhost", "127.0.0.1", "example.com", "example.org") or parts.hostname.endswith((".test", ".invalid")):
        raise ValueError("Indica el dominio definitivo, no un dominio de prueba.")
    documents = []
    urls = []
    for page in PAGES:
        path = root / page
        source = path.read_text(encoding="utf-8")
        url = base_url + ("/" if page == "index.html" else "/" + page)
        urls.append(url)
        block = '\n'.join([
            '<!-- SEO:START -->',
            f'<link rel="canonical" href="{html.escape(url, quote=True)}">',
            f'<meta property="og:url" content="{html.escape(url, quote=True)}">',
            f'<meta property="og:image" content="{html.escape(base_url, quote=True)}/assets/images/social-card.png">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta property="og:image:alt" content="Reparabrisas: reparación de parabrisas a domicilio en la zona norte de la Región Metropolitana">',
            f'<meta name="twitter:image" content="{html.escape(base_url, quote=True)}/assets/images/social-card.png">',
            '<!-- SEO:END -->',
        ])
        source, count = re.subn(r'<!-- SEO:START -->.*?<!-- SEO:END -->', lambda _: block, source, flags=re.S)
        if count != 1:
            raise ValueError(f"Falta un bloque SEO único en {page}")

        def add_schema_url(match):
            schema = json.loads(match.group(1))
            schema["url"] = url
            if schema.get("@type") == "AutoRepair":
                schema["@id"] = base_url + "/#negocio"
                schema["image"] = base_url + "/assets/images/social-card.png"
            elif "provider" in schema:
                schema["provider"]["@id"] = base_url + "/#negocio"
                schema["provider"]["url"] = base_url + "/"
            return '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c") + '</script>'

        source = re.sub(r'<script type="application/ld\+json">(.*?)</script>', add_schema_url, source, flags=re.S)
        documents.append((path, source))
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{escape(url)}</loc></url>\n' for url in urls) + '</urlset>\n'
    for path, source in documents:
        path.write_text(source, encoding="utf-8")
    (root / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (root / "robots.txt").write_text(f'User-agent: *\nAllow: /\n\nSitemap: {base_url}/sitemap.xml\n', encoding="utf-8")
    print("SEO configurado para", base_url, "· No se ha publicado ningún archivo.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="URL definitiva HTTPS; puede incluir subcarpeta de GitHub Pages.")
    args = parser.parse_args()
    try:
        configure(ROOT, args.base_url)
    except ValueError as error:
        parser.error(str(error))
