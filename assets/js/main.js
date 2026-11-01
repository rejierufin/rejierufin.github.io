/* ==========================================================================
   Rejie Rufin — portfolio interactions
   Vanilla JS, no dependencies. Everything degrades gracefully if it fails.
   ========================================================================== */
(function () {
  "use strict";

  var doc = document;
  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  doc.documentElement.classList.add("js");

  /* ---------------- Sticky header state ---------------- */
  var header = doc.getElementById("siteHeader");
  var toTop = doc.getElementById("toTop");

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-scrolled", y > 8);
    if (toTop) {
      var show = y > 520;
      toTop.hidden = !show;
      // Allow the browser to paint the display change before fading in.
      if (show) window.requestAnimationFrame(function () { toTop.classList.add("is-visible"); });
      else toTop.classList.remove("is-visible");
    }
  }

  /* ---------------- Mobile navigation ---------------- */
  var nav = doc.getElementById("primaryNav");
  var navToggle = doc.getElementById("navToggle");
  var mqDesktop = window.matchMedia("(min-width: 981px)");

  function closeNav() {
    if (!nav || !navToggle) return;
    nav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
    navToggle.setAttribute("aria-label", "Open navigation menu");
    doc.body.classList.remove("is-locked");
  }

  function openNav() {
    if (!nav || !navToggle) return;
    nav.classList.add("is-open");
    navToggle.setAttribute("aria-expanded", "true");
    navToggle.setAttribute("aria-label", "Close navigation menu");
    doc.body.classList.add("is-locked");
  }

  if (nav && navToggle) {
    navToggle.addEventListener("click", function () {
      if (nav.classList.contains("is-open")) closeNav();
      else openNav();
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeNav();
    });

    doc.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("is-open")) {
        closeNav();
        navToggle.focus();
      }
    });

    var onBreakpoint = function (event) { if (event.matches) closeNav(); };
    if (mqDesktop.addEventListener) mqDesktop.addEventListener("change", onBreakpoint);
    else mqDesktop.addListener(onBreakpoint);
  }

  /* ---------------- Active navigation state ---------------- */
  var navLinks = Array.prototype.slice.call(doc.querySelectorAll(".nav__link"));
  var sections = navLinks
    .map(function (link) {
      var id = link.getAttribute("href");
      var el = id && id.charAt(0) === "#" ? doc.querySelector(id) : null;
      return el ? { link: link, el: el } : null;
    })
    .filter(Boolean);

  function setActive(id) {
    navLinks.forEach(function (link) {
      var isActive = link.getAttribute("href") === "#" + id;
      link.classList.toggle("is-active", isActive);
      if (isActive) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
  }

  function updateActive() {
    if (!sections.length) return;
    var offset = (header ? header.offsetHeight : 0) + 90;
    var y = (window.scrollY || window.pageYOffset) + offset;
    var current = sections[0].el.id;
    var atBottom =
      window.innerHeight + (window.scrollY || window.pageYOffset) >=
      doc.documentElement.scrollHeight - 4;

    sections.forEach(function (item) {
      if (item.el.offsetTop <= y) current = item.el.id;
    });
    if (atBottom) current = sections[sections.length - 1].el.id;
    setActive(current);
  }

  /* ---------------- Scroll listener (rAF throttled) ---------------- */
  var ticking = false;
  function requestScrollUpdate() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      onScroll();
      updateActive();
      ticking = false;
    });
  }

  window.addEventListener("scroll", requestScrollUpdate, { passive: true });
  window.addEventListener("resize", requestScrollUpdate);
  onScroll();
  updateActive();

  /* ---------------- Back to top ---------------- */
  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: prefersReducedMotion.matches ? "auto" : "smooth" });
      var skip = doc.querySelector(".skip-link");
      if (skip) skip.focus({ preventScroll: true });
      else doc.body.focus();
    });
  }

  /* ---------------- Section reveal ---------------- */
  var revealItems = Array.prototype.slice.call(doc.querySelectorAll(".reveal"));

  if ("IntersectionObserver" in window && !prefersReducedMotion.matches) {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-inview");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );
    revealItems.forEach(function (item) { revealObserver.observe(item); });
  } else {
    revealItems.forEach(function (item) { item.classList.add("is-inview"); });
  }

  /* ---------------- Portrait photo detection ----------------
     CSS shows a designed monogram panel until the portrait file exists.
     The hero image is /profile-photo.jpg; once it loads, the monogram panel
     behind it fades out and the photo fades in.
  ------------------------------------------------------------- */
  var portrait = doc.getElementById("portrait");
  var portraitImg = portrait ? portrait.querySelector(".portrait__img") : null;

  if (portraitImg) {
    var portraitSources = [
      "/profile-photo.jpg"
    ];
    var portraitIndex = 0;
    var portraitFound = false;

    var showPortrait = function () {
      if (portraitImg.naturalWidth > 0) {
        portraitFound = true;
        if (portrait) portrait.classList.add("portrait--has-photo");
      }
    };

    // Try the next file format until one loads; if none exist, keep the monogram panel.
    var tryPortrait = function (index) {
      if (portraitFound || index >= portraitSources.length || index <= portraitIndex) return;
      portraitIndex = index;
      var probe = new Image();
      probe.onload = function () { portraitImg.src = probe.src; };
      probe.onerror = function () { tryPortrait(index + 1); };
      probe.src = portraitSources[index];
    };

    portraitImg.addEventListener("load", showPortrait);
    portraitImg.addEventListener("error", function () {
      // If the photo is ever missing, fall back to the monogram panel.
      if (portrait) portrait.classList.add("portrait--no-photo");
    });

    if (portraitImg.complete) {
      if (portraitImg.naturalWidth > 0) showPortrait();
      else tryPortrait(1);
    }
  }

  /* ---------------- Project dialogs ---------------- */
  var dialog = doc.getElementById("projectDialog");

  if (dialog && typeof dialog.showModal === "function") {
    var dCategory = dialog.querySelector("[data-dialog-category]");
    var dTitle = dialog.querySelector("[data-dialog-title]");
    var dDesc = dialog.querySelector("[data-dialog-desc]");
    var dTags = dialog.querySelector("[data-dialog-tags]");
    var dStatus = dialog.querySelector("[data-dialog-status]");
    var dContact = dialog.querySelector("[data-dialog-contact]");

    function fillDialog(card) {
      var data = card.dataset;
      dCategory.textContent = data.category || "";
      dTitle.textContent = data.title || "";
      dDesc.textContent = data.details || data.desc || "";
      dStatus.textContent = data.status || "";
      dTags.innerHTML = "";
      (data.tags || "")
        .split(",")
        .map(function (tag) { return tag.trim(); })
        .filter(Boolean)
        .forEach(function (tag) {
          var li = doc.createElement("li");
          li.textContent = tag;
          dTags.appendChild(li);
        });
    }

    Array.prototype.forEach.call(doc.querySelectorAll("[data-project-open]"), function (button) {
      button.addEventListener("click", function () {
        var card = button.closest(".project-card");
        if (!card) return;
        fillDialog(card);
        dialog.showModal();
      });
    });

    Array.prototype.forEach.call(dialog.querySelectorAll("[data-dialog-close]"), function (button) {
      button.addEventListener("click", function () { dialog.close(); });
    });

    if (dContact) {
      dContact.addEventListener("click", function () { dialog.close(); });
    }

    // Close when clicking the backdrop (the dialog element itself, outside .dialog__inner)
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) {
        var rect = dialog.getBoundingClientRect();
        var inside =
          event.clientX >= rect.left &&
          event.clientX <= rect.right &&
          event.clientY >= rect.top &&
          event.clientY <= rect.bottom;
        if (!inside) dialog.close();
      }
    });
  }

  /* ---------------- Optional social links ----------------
     Any .social anchor with a non-empty data-href becomes a live link.
     Empty data-href keeps the chip disabled, so no broken URLs ship.
  ------------------------------------------------------------- */
  Array.prototype.forEach.call(doc.querySelectorAll(".social[data-social]"), function (link) {
    var url = (link.getAttribute("data-href") || "").trim();
    if (!url) return;
    link.setAttribute("href", url);
    link.removeAttribute("aria-disabled");
    link.removeAttribute("tabindex");
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noopener noreferrer");
    link.setAttribute("aria-label", link.getAttribute("data-social") + " profile (opens in a new tab)");
  });

  /* ---------------- Footer year ---------------- */
  Array.prototype.forEach.call(doc.querySelectorAll("[data-current-year]"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
