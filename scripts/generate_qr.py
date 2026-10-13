#!/usr/bin/env python3
"""Generate print-friendly SVG QR codes for every public page of the Golu site.

Pages discovered automatically:
  index.html                 -> qr-codes/home.svg
  stories/<slug>.html        -> qr-codes/stories--<slug>.svg
  pages/<name>.html          -> qr-codes/pages--<name>.svg   (optional extra pages)

The base public URL is read from site.json unless --base-url is given.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, urlsplit

import qrcode
from qrcode.image.svg import SvgPathImage


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDERS = ("YOUR-USERNAME", "YOUR-REPO", "USERNAME", "REPO")


def read_base_url(cli_value: str | None) -> str:
    if cli_value:
        return cli_value
    config = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
    return config["base_url"]


def manifest_slugs() -> list[str]:
    """Read the slugs listed in assets/js/stories.js (the story index)."""
    text = (ROOT / "assets/js/stories.js").read_text(encoding="utf-8")
    return re.findall(r'slug:\s*"([^"]+)"', text)


def collect_pages() -> list[Path]:
    pages = [ROOT / "index.html"]
    # Files starting with "_" (such as templates) are not public story pages.
    pages += sorted(p for p in (ROOT / "stories").glob("*.html") if not p.name.startswith("_"))
    if (ROOT / "pages").is_dir():
        pages += sorted((ROOT / "pages").rglob("*.html"))
    return pages


def check_stories_match_index(story_files: list[Path]) -> None:
    listed = set(manifest_slugs())
    on_disk = {p.stem for p in story_files}
    missing_files = sorted(listed - on_disk)
    unlisted = sorted(on_disk - listed)
    if missing_files:
        sys.exit(
            "Error: these stories are listed in assets/js/stories.js but have no page "
            f"in stories/: {', '.join(missing_files)}"
        )
    for slug in unlisted:
        print(f"Warning: stories/{slug}.html exists but is not listed in assets/js/stories.js; "
              "it will get a QR code but will not appear in navigation.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", help="Override the base URL in site.json.")
    parser.add_argument("--output-dir", default=str(ROOT / "qr-codes"),
                        help="Where to write SVG files (default: qr-codes/).")
    args = parser.parse_args()

    base_url = read_base_url(args.base_url)
    base = base_url.rstrip("/") + "/"
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.netloc or parsed.query or parsed.fragment:
        parser.error("the base URL must be a public HTTPS URL, with no query or fragment")
    if any(token in base for token in PLACEHOLDERS):
        parser.error("replace the example YOUR-USERNAME / YOUR-REPO placeholders in site.json "
                     "with your real GitHub Pages URL before generating printable QR codes")

    story_files = sorted((ROOT / "stories").glob("*.html"))
    story_files = [p for p in story_files if not p.name.startswith("_")]
    check_stories_match_index(story_files)

    pages = collect_pages()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = set()
    for page in pages:
        relative = page.relative_to(ROOT).as_posix()
        url = base if relative == "index.html" else base + quote(relative, safe="/")
        name = "home" if relative == "index.html" else relative.removesuffix(".html").replace("/", "--")
        output = output_dir / f"{name}.svg"

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr.make_image(image_factory=SvgPathImage).save(output)
        generated.add(output.name)
        print(f"{relative:<36} → {output.name:<32} {url}")

    stale = sorted(p.name for p in output_dir.glob("*.svg") if p.name not in generated)
    if stale:
        print("\nNote: these SVGs are not from the current pages (renamed or removed?). "
              "Delete them if they are no longer needed:\n  " + "\n  ".join(stale))

    print(f"\nGenerated {len(pages)} QR code(s). Test each with a phone before printing.")


if __name__ == "__main__":
    main()
