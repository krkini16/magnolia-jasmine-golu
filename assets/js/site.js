/*
 * Builds the shared navigation and story lists from assets/js/stories.js.
 * Edit stories.js to change what appears; you should not need to edit this file.
 *
 * Pages opt in with attributes on <body> and on containers:
 *   <body data-root="./" data-page="home">          homepage
 *   <body data-root="../" data-story="my-slug">     story page
 *   <aside data-sidebar>                            sidebar, filled in here
 *   <div data-story-cards>                          homepage story cards
 *   <nav data-related>                              "more stories" on story pages
 */
(function () {
  "use strict";

  var body = document.body;
  // "./" on the homepage, "../" on story pages — keeps links working on a
  // GitHub Pages subpath such as /my-repo/.
  var root = body.dataset.root || "./";
  var currentStory = body.dataset.story || "";
  var isHome = body.dataset.page === "home";
  var stories = window.GOLU_STORIES || [];

  function storyHref(story) {
    return root + "stories/" + story.slug + ".html";
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) {
      node.setAttribute(key, attrs[key]);
    });
    (children || []).forEach(function (child) {
      node.append(typeof child === "string" ? document.createTextNode(child) : child);
    });
    return node;
  }

  function buildSidebar() {
    var aside = document.querySelector("[data-sidebar]");
    if (!aside) return;

    var nav = el("nav", { id: "site-nav", class: "site-nav", "aria-label": "Golu" });

    var toggle = el("button", {
      class: "nav-toggle",
      type: "button",
      "aria-expanded": "false",
      "aria-controls": "site-nav"
    }, ["Menu"]);
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? "Close" : "Menu";
    });

    var head = el("div", { class: "sidebar-head" }, [
      el("a", { class: "brand", href: root }, ["Golu"]),
      toggle
    ]);

    var homeLink = el("a", { href: root }, ["Home"]);
    var aboutLink = el("a", { href: root + "#about" }, ["About Golu"]);
    if (isHome) {
      homeLink.setAttribute("aria-current", "page");
    }

    var list = el("ul", {}, [
      el("li", {}, [homeLink]),
      el("li", {}, [aboutLink])
    ]);

    var storyItems = stories.map(function (story) {
      var link = el("a", { href: storyHref(story) }, [story.title]);
      if (story.slug === currentStory) {
        link.setAttribute("aria-current", "page");
      }
      return el("li", {}, [link]);
    });

    nav.append(
      list,
      el("p", { class: "nav-label" }, ["Stories"]),
      el("ul", {}, storyItems)
    );

    aside.append(head, nav);
  }

  function storyCard(story) {
    var img = el("img", {
      src: root + story.cover,
      alt: "",
      loading: "lazy"
    });
    return el("a", { class: "story-card", href: storyHref(story) }, [
      el("div", { class: "thumb" }, [img]),
      el("div", { class: "story-card-body" }, [
        el("h3", {}, [story.title]),
        el("p", {}, [story.summary]),
        el("span", { class: "more" }, ["Read the story →"])
      ])
    ]);
  }

  function fillStoryCards() {
    var container = document.querySelector("[data-story-cards]");
    if (!container) return;
    container.append.apply(container, stories.map(storyCard));
  }

  function fillRelated() {
    var container = document.querySelector("[data-related]");
    if (!container) return;

    var others = stories.filter(function (story) {
      return story.slug !== currentStory;
    });
    if (others.length === 0) return;

    container.append(
      el("h2", {}, ["More stories"]),
      el("div", { class: "story-cards" }, others.map(storyCard))
    );
  }

  buildSidebar();
  fillStoryCards();
  fillRelated();
})();
