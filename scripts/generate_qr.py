#!/usr/bin/env python3
"""Generate print-friendly SVG QR codes for all public HTML pages."""

import argparse
from pathlib import Path
from urllib.parse import quote, urlsplit

import qrcode
from qrcode.image.svg import SvgPathImage


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        required=True,
        help="Final public site URL, including the repository path if needed.",
    )
    args = parser.parse_args()

    base = args.base_url.rstrip("/") + "/"
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.netloc or parsed.query or parsed.fragment:
        parser.error("--base-url must be a public HTTPS URL, with no query or fragment")
    if "USERNAME" in base or "REPO" in base:
        parser.error("Replace the example USERNAME/REPO placeholders with your real URL")

    pages = [ROOT / "index.html", *sorted((ROOT / "pages").rglob("*.html"))]
    output_dir = ROOT / "qr-codes"
    output_dir.mkdir(exist_ok=True)

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
        print(f"{output.relative_to(ROOT)}  →  {url}")

    print(f"\nGenerated {len(pages)} QR code(s). Test each with a phone before printing.")


if __name__ == "__main__":
    main()
