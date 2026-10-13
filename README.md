# Golu website

A small, static website about **Golu** (also called Kolu or Bommai Golu), the South
Indian Navaratri tradition of arranging dolls and figurines on tiered steps. The
homepage introduces the tradition. Each story page explores one figure or scene
from a display.

The site is plain HTML, CSS, and a little vanilla JavaScript. It needs no
backend, framework, database, or build step, and it deploys directly to GitHub
Pages. A small script still generates printable QR codes for each page.

## Repository structure

```text
index.html                         Homepage: hero, "What is Golu?", story cards
stories/                           One HTML file per story (the public story pages)
  durga-and-mahishasura.html         sample story
  ganesha-and-the-mooshika.html      sample story
  saraswati-and-the-veena.html       sample story
templates/story-template.html      Copy this to start a new story
assets/
  styles.css                       All styling (colours and fonts are at the top)
  js/stories.js                    THE STORY INDEX: the one list of stories
  js/site.js                       Builds the sidebar and story lists (rarely edited)
  images/golu-hero.svg             Homepage illustration (placeholder)
  images/stories/<slug>/           Photographs and images, one folder per story
scripts/generate_qr.py             Creates the printable QR codes
site.json                          The public website address (used for QR codes)
qr-codes/                          Generated QR codes (SVG)
requirements.txt                   Python dependency for the QR script
.nojekyll                          Tells GitHub Pages to serve files as they are
```

## Preview locally

From the repository folder, start a simple web server:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/>. Refresh the page after each change.

## Edit the homepage introduction

- **Hero text** (heading and opening line): in `index.html`, in the section marked
  `<!-- HERO -->`.
- **"What is Golu?"** text: in `index.html`, in the section marked
  `<!-- WHAT IS GOLU? -->`. It is ordinary paragraphs wrapped in `<p>…</p>`.
  Edit the words between the tags and keep the tags.
- **Hero illustration**: replace `assets/images/golu-hero.svg` with your own image
  (same file name), or change the `src` in `index.html` to a new file.

## Add a new story

This is the workflow you will use most. Here is an example of adding a fourth
story called *Lakshmi and the Lotus*.

**1. Choose a slug.** The slug is the story's permanent web address and must
be lowercase, with hyphens and no spaces: `lakshmi-and-the-lotus`. Choose it
carefully, because the QR code for the story points to it.

**2. Copy the template** to the `stories/` folder:

```bash
cp templates/story-template.html stories/lakshmi-and-the-lotus.html
```

**3. Edit the new file.** Open `stories/lakshmi-and-the-lotus.html` in any text
editor and replace every line marked `REPLACE`:

- `<title>` and the `<meta name="description">`
- `data-story="…"` in the `<body>` tag: put the slug there (it highlights the
  page in the sidebar)
- `<h1>`, the optional `subtitle` line, and the section headings and paragraphs
- the image `src` and `alt` text, and the captions

Add or remove `<h2>` sections and `<p>` paragraphs as needed. Each image is one
`<figure class="plate">` block. To remove an image, delete the whole block.

**4. Add your photographs** to `assets/images/stories/lakshmi-and-the-lotus/`
(create the folder). See *Add and replace photographs* below.

**5. Add the story to the index.** Open `assets/js/stories.js` and add an entry
to the list. Keep the entries separated by commas:

```js
  {
    slug: "lakshmi-and-the-lotus",
    title: "Lakshmi and the Lotus",
    summary: "A short sentence shown on the homepage card.",
    cover: "assets/images/stories/lakshmi-and-the-lotus/cover.jpg",
    coverAlt: "Descriptive text for the card image"
  }
```

The `title` and `slug` must match the story file. The sidebar, the homepage card,
and the "More stories" section at the bottom of each story are all generated from
this list, so they update automatically. The order of entries is the order shown.

**6. Check it.** Run the local preview and open the new story. Then regenerate the
QR codes (see *Generate QR codes* below) and push your changes.

Rules of thumb:

- **Do not rename a story file after its QR code is printed.** Renaming changes the
  address, and the printed code would then lead to a missing page. Editing the
  text, images, or title never changes the address, so those edits are always safe.
- Story files whose names start with `_` (such as `_draft.html`) get no QR code and
  are not listed on the site. They are still published if you push them, so do not
  use them for private material.

## Add and replace photographs

Put images in the folder for their story:

```text
assets/images/stories/<slug>/
  cover.jpg          the main photograph (the card image and the first image on the page)
  01-steps.jpg       supporting photographs, numbered in the order they appear
  02-detail.jpg
```

Supported formats are **JPG**, **PNG**, and **WebP**. Use lowercase file names
with no spaces; a hyphen (`01-steps.jpg`) is fine.

Tips:

- Around **1600 px on the longest side** is a good size for a web page. Very large
  photographs slow the site down on phones. Resize large originals before uploading.
- The page displays photographs at their natural proportions. They are not cropped.
  On the homepage, cards show the whole image on a neutral background.
- Reference an image from a story page with a path relative to the page:
  `../assets/images/stories/<slug>/cover.jpg`. From the homepage, use
  `assets/images/…` without the `../`.
- Always write descriptive `alt` text: what someone would see if they could not
  see the picture, for example *"Three tiers of dolls with a lamp at the base"*.
  If an image is purely decorative, use `alt=""`.
- To **replace** a photograph, overwrite the file with the same name, or change the
  `src` in the story file. If the card image changes, also update `cover` in
  `assets/js/stories.js`.
- The current `.svg` files are placeholder illustrations. You can delete them once
  you have real photographs and point the `src` to your `.jpg` files.

## Generate QR codes

Each page has its own QR code. Generate QR codes **after** adding or renaming a
story, and after you have settled the final website address.

**1. Set your public address** in `site.json`:

```json
{
  "base_url": "https://YOUR-USERNAME.github.io/YOUR-REPO/"
}
```

Replace `YOUR-USERNAME` and `YOUR-REPO` with your GitHub details, for example
`https://jane.github.io/golu/`. A custom domain works too. The script refuses to
run while the placeholders are still in place.

**2. Install the one dependency** (only needed once):

```bash
python3 -m pip install -r requirements.txt
```

**3. Generate the codes:**

```bash
python3 scripts/generate_qr.py
```

The script finds every page automatically and writes one SVG per page:

```text
qr-codes/home.svg                              → the homepage
qr-codes/stories--durga-and-mahishasura.svg    → a story page
qr-codes/stories--<slug>.svg                   → one file per story
```

It also checks that every story page in `stories/` appears in `assets/js/stories.js`
and warns you if one does not. If a file in `qr-codes/` belongs to a story you
removed, the script lists it so you can delete it.

To test the output somewhere other than the real folder, add
`--output-dir /some/other/folder`. To use a different address for one run, add
`--base-url https://…/`.

**4. Test before printing.** Scan each code with a phone and confirm it opens the
right page on your published site. SVG files stay sharp at any print size.

## Publish with GitHub Pages

1. Create a **public** repository on GitHub (for example, `golu`). Pages is free for
   public repositories.
2. Push this folder to the repository's `main` branch.
3. On GitHub, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**, select `main`,
   and select the `/ (root)` folder. Click **Save**.
5. After a minute or two, the site is live at
   `https://YOUR-USERNAME.github.io/YOUR-REPO/`.

To **update** the site, edit files and push them to `main`. GitHub Pages republishes
automatically. Every link and image in the site is relative, so the site works
under the repository path. Do not add links that start with `/`, because those
would point to the top of your GitHub account rather than to your site.

## Limitations and assumptions

- **Sample content.** The three story pages (*Durga and the Buffalo Demon*,
  *Ganesha and the Mooshika*, *Saraswati and the Veena*) are examples of
  mythological background, written to show the layout. The "What is Golu?"
  introduction is general and should be checked and edited to suit your display.
  Each is marked "Sample story" on its page. Replace them with your own text.
- **Placeholder images.** The illustrations are simple SVG artwork, not photographs.
- **JavaScript is needed for the navigation.** The sidebar, the story cards, and the
  "More stories" section are filled in by `assets/js/site.js`. If JavaScript is
  turned off, the navigation and cards will not appear. The text and images in each
  story page still show.
- **Fonts** come from Google Fonts (Cormorant Garamond and Source Sans 3). If the
  connection fails, the page falls back to a standard serif or sans-serif font.
- **Light theme only.** The design is fixed to a light background.
- **Public content.** Everything in a public repository, including photographs and
  text, is visible to anyone. Do not include private information, and check that
  you have permission to publish each photograph.
- **Static site.** GitHub Pages cannot process forms, logins, or a database. If you
  need those later, a separate service would be required.
- GitHub's terms restrict some commercial uses of Pages. Check them if you plan
  anything beyond a personal or cultural site.
