/*
 * THE STORY INDEX — the only place you need to edit to add, remove, or
 * rename a story.
 *
 * The sidebar, the homepage story cards, and the "more stories" list at the
 * bottom of each story are all generated from this list.
 *
 * Each entry:
 *   slug   – the page name. Story page = stories/<slug>.html.
 *            Never change it after printing a QR code for that story.
 *   title  – shown in the sidebar and on cards. Keep it in sync with the <h1>
 *            in the story's HTML file.
 *   summary – one or two sentences shown on the homepage card.
 *   cover  – the card image, a path from the site root. Usually the same file
 *            as the story's main image.
 *   coverAlt – description of the card image.
 *
 * Order here is the order shown in the sidebar and on the homepage.
 */
window.GOLU_STORIES = [
  {
    slug: "durga-and-mahishasura",
    title: "Durga and the Buffalo Demon",
    summary: "How the goddess Durga, born from the combined energy of the gods, overcame the shape-shifting demon Mahishasura.",
    cover: "assets/images/stories/durga-and-mahishasura/cover.svg",
    coverAlt: "Placeholder illustration of a crowned goddess with many arms beside a lion"
  },
  {
    slug: "ganesha-and-the-mooshika",
    title: "Ganesha and the Mooshika",
    summary: "How the elephant-headed Ganesha subdued a proud demon, who became the small mouse that carries him.",
    cover: "assets/images/stories/ganesha-and-the-mooshika/cover.svg",
    coverAlt: "Placeholder illustration of an elephant-headed figure with a small mouse at its feet"
  },
  {
    slug: "saraswati-and-the-veena",
    title: "Saraswati and the Veena",
    summary: "The goddess of learning and music, whose veena and books are honoured in the final days of Navaratri.",
    cover: "assets/images/stories/saraswati-and-the-veena/cover.svg",
    coverAlt: "Placeholder illustration of a veena surrounded by lotus flowers"
  }
];
