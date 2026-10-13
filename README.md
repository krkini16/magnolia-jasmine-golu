# QR-linked static website

A lightweight, mobile-friendly website for GitHub Pages. It contains plain HTML,
CSS, one replaceable illustration, and a script that produces printable SVG QR
codes. The public website needs **no backend, JavaScript framework, or database**.

## Files

```text
index.html                  Homepage
pages/example.html          Example content page (copy this to add pages)
assets/styles.css           Shared styling
assets/images/sample.svg    Replaceable example image
scripts/generate_qr.py      Creates QR codes for every HTML page
qr-codes/                   Generated, printable SVG QR codes
requirements.txt            One local QR-generation dependency
.nojekyll                   Serve files directly on GitHub Pages
```

## Publish on GitHub Pages (no command line needed)

1. Create a **public** GitHub repository, e.g. `my-qr-site`.
2. Upload the **contents of this folder** to the repository root (so `index.html`
   appears at the top level).
3. In the repository, go to **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**, then `main`
   and `/ (root)`. Save.
5. Once published, your site will usually be at
   `https://YOUR-USERNAME.github.io/my-qr-site/`. A repository named
   `YOUR-USERNAME.github.io` instead publishes at
   `https://YOUR-USERNAME.github.io/`.

You can also connect a custom domain in Settings → Pages. If you plan to print
QR codes, **settle on the final URL first**.

## Edit or add content

- Edit `index.html` for the homepage.
- Edit `pages/example.html` for the sample content page.
- To add a page, copy `pages/example.html` to `pages/new-page.html`, change its
  title/content, then add a link to `pages/new-page.html` on `index.html`.
- Put images in `assets/images/` and refer to them using relative paths:
  `assets/images/photo.jpg` from the homepage, or
  `../assets/images/photo.jpg` from a page inside `pages/`.
- Make changes in GitHub's browser-based editor if you prefer not to use Git.

Every edit to the published branch automatically triggers a site update.
Changing a page's text or images **does not change its QR code**. Moving or
renaming the page, changing the domain, or changing the repository path **does**.

## Generate the QR codes

The QR generator runs locally and creates one SVG per page, including the
homepage. An SVG stays sharp when printed at large or small sizes.

Once Python is installed, run these commands in this folder:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/generate_qr.py --base-url https://YOUR-USERNAME.github.io/my-qr-site/
```

**Replace the URL** with the actual live site URL. If you use a custom domain,
pass that instead, e.g. `--base-url https://example.com/`.

Generated files will appear in `qr-codes/`:

```text
qr-codes/home.svg
qr-codes/pages--example.svg
```

You can download/print these, upload them to the repository if you want them
versioned, or use them in a flyer/design tool. Generate them again after adding
pages. Test each QR code with your phone before printing.

## Preview locally (optional)

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000/`.

## Important limitations

- Site content and files in a public repository are public: do not commit
  passwords, private data, or credentials.
- GitHub Pages serves static files. Forms, logins, or a database need another
  service.
- GitHub restricts using Pages as free hosting for a commercial transaction
  site or commercial SaaS; check GitHub's terms if that's your intended use.
