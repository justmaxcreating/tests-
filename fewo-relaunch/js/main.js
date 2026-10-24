/* Ferienwohnungen Voll – Interaktionen (kein Framework, ~progressive enhancement) */
(() => {
  const root = document.documentElement;
  root.classList.remove("no-js");
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Header: Blur beim Scrollen ---------- */
  const header = $(".site-header");
  const onScroll = () => header && header.classList.toggle("is-scrolled", scrollY > 8);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile Navigation ---------- */
  const toggle = $(".menu-toggle");
  const mobileNav = $(".mobile-nav");
  if (toggle && mobileNav) {
    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      mobileNav.classList.toggle("is-open", open);
    };
    toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
    $$("a", mobileNav).forEach((a) => a.addEventListener("click", () => setOpen(false)));
    addEventListener("keydown", (e) => e.key === "Escape" && setOpen(false));
  }

  /* ---------- Navigation: gleitende Hover-Pille ---------- */
  const nav = $(".nav");
  const pill = $(".nav-pill");
  if (nav && pill) {
    const moveTo = (a) => {
      pill.style.width = `${a.offsetWidth}px`;
      pill.style.transform = `translateX(${a.offsetLeft}px)`;
      pill.style.opacity = "1";
    };
    $$("a", nav).forEach((a) => {
      a.addEventListener("mouseenter", () => moveTo(a));
      a.addEventListener("focus", () => moveTo(a));
    });
    nav.addEventListener("mouseleave", () => (pill.style.opacity = "0"));
  }

  /* ---------- Buttons: Lichtpunkt folgt dem Cursor ---------- */
  $$(".btn").forEach((btn) => {
    btn.addEventListener("pointermove", (e) => {
      const r = btn.getBoundingClientRect();
      btn.style.setProperty("--mx", `${e.clientX - r.left}px`);
      btn.style.setProperty("--my", `${e.clientY - r.top}px`);
    });
  });

  /* ---------- Reveal on scroll ---------- */
  const reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add("is-in");
            io.unobserve(en.target);
          }
        }),
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-in"));
  }

  /* ---------- Toast ---------- */
  const toast = $(".toast");
  let toastTimer;
  const showToast = (msg) => {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 2400);
  };

  /* ---------- Gäste-Stepper ---------- */
  $$("[data-stepper]").forEach((st) => {
    const input = $("input", st);
    const out = $("output", st);
    const [minus, plus] = $$("button", st);
    const min = Number(st.dataset.min || 1);
    const max = Number(st.dataset.max || 6);
    const render = () => {
      const v = Number(input.value);
      out.textContent = v;
      minus.disabled = v <= min;
      plus.disabled = v >= max;
      out.classList.remove("bump");
      void out.offsetWidth;
      out.classList.add("bump");
      st.dispatchEvent(new CustomEvent("change", { bubbles: true }));
    };
    minus.addEventListener("click", () => {
      input.value = Math.max(min, Number(input.value) - 1);
      render();
    });
    plus.addEventListener("click", () => {
      input.value = Math.min(max, Number(input.value) + 1);
      render();
    });
    st.setMax = (m) => {
      st.dataset.max = m;
      if (Number(input.value) > m) input.value = m;
      plus.disabled = Number(input.value) >= m;
      minus.disabled = Number(input.value) <= min;
      out.textContent = input.value;
    };
    minus.disabled = Number(input.value) <= min;
    plus.disabled = Number(input.value) >= max;
  });

  /* ---------- Datumslogik: Abreise ≥ Anreise + 1, Nächte berechnen ---------- */
  const iso = (d) => d.toISOString().slice(0, 10);
  const today = iso(new Date());
  const fmt = new Intl.DateTimeFormat("de-DE", { day: "numeric", month: "short" });
  $$("[data-dates]").forEach((scope) => {
    const inEl = $("[data-date-in]", scope);
    const outEl = $("[data-date-out]", scope);
    const nightsEl = $("[data-nights]", scope);
    if (!inEl || !outEl) return;
    inEl.min = today;
    outEl.min = today;
    const update = () => {
      if (inEl.value) {
        const next = new Date(inEl.value);
        next.setDate(next.getDate() + 1);
        outEl.min = iso(next);
        if (outEl.value && outEl.value <= inEl.value) outEl.value = iso(next);
      }
      if (nightsEl) {
        if (inEl.value && outEl.value) {
          const n = Math.round((new Date(outEl.value) - new Date(inEl.value)) / 864e5);
          nightsEl.innerHTML = `<strong>${n} ${n === 1 ? "Nacht" : "Nächte"}</strong><span>${fmt.format(new Date(inEl.value))} – ${fmt.format(new Date(outEl.value))}</span>`;
        } else {
          nightsEl.textContent = nightsEl.dataset.empty || "";
        }
      }
    };
    inEl.addEventListener("change", () => {
      update();
      if (!outEl.value && outEl.showPicker) {
        try {
          outEl.showPicker();
        } catch (_) {}
      }
    });
    outEl.addEventListener("change", update);
    update();
  });

  /* ---------- Wohnungs-Auswahl begrenzt Gästezahl ---------- */
  $$("[data-unit-select]").forEach((sel) => {
    const st = $("[data-stepper]", sel.closest("form"));
    const apply = () => {
      const opt = sel.selectedOptions[0];
      if (st && st.setMax && opt && opt.dataset.max) st.setMax(Number(opt.dataset.max));
    };
    sel.addEventListener("change", apply);
    apply();
  });

  /* ---------- Startseite: Buchungsleiste füllt Anfrageformular vor ---------- */
  const bar = $("[data-booking-bar]");
  const inquiry = $("#anfrage-form");
  if (bar && inquiry) {
    bar.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = new FormData(bar);
      const set = (name, val) => {
        const el = inquiry.elements[name];
        if (el && val) {
          el.value = val;
          el.dispatchEvent(new Event("change", { bubbles: true }));
        }
      };
      const place = data.get("ort");
      if (place) set("wohnung", place === "wuerzburg" ? "Würzburg – Das Herzstück der Altstadt" : "Thüngen – egal welche");
      set("anreise", data.get("anreise"));
      set("abreise", data.get("abreise"));
      const guests = data.get("gaeste");
      const gInput = inquiry.querySelector("[data-stepper] input");
      if (guests && gInput) {
        gInput.value = guests;
        $("output", gInput.closest("[data-stepper]")).textContent = guests;
      }
      $("#anfrage").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
      setTimeout(() => inquiry.elements.name && inquiry.elements.name.focus({ preventScroll: true }), 650);
    });
  }

  /* ---------- Wohnungskarten „Anfragen“ wählen die Wohnung im Formular vor ---------- */
  $$("[data-unit]").forEach((a) =>
    a.addEventListener("click", () => {
      const sel = $("#anfrage-form [data-unit-select]");
      if (!sel) return;
      sel.value = a.dataset.unit;
      sel.dispatchEvent(new Event("change", { bubbles: true }));
    })
  );

  /* ---------- Detailseite: Buchungskarte klappt erst die Kontaktfelder auf ---------- */
  const expandBookCard = (form) => {
    const more = $(".book-more", form);
    if (!more || more.classList.contains("is-open")) return false;
    const dates = $$("[data-date-in], [data-date-out]", form);
    if (!dates.every((d) => d.reportValidity())) return true;
    more.classList.add("is-open");
    more.removeAttribute("inert");
    $("[data-book-next] .btn-label", form).textContent = "Anfrage senden";
    setTimeout(() => $("input", more).focus({ preventScroll: true }), 350);
    return true;
  };

  /* ---------- Anfrageformulare (Netlify Forms, mit Demo-Modus lokal) ---------- */
  const isDemo = location.protocol === "file:" || /^(localhost|127\.|0\.0\.0\.0)/.test(location.hostname);
  $$("form[data-inquiry]").forEach((form) => {
    const status = $(".form-status", form);
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (expandBookCard(form)) return;
      if (!form.reportValidity()) return;
      const submit = $("button[type=submit]", form);
      submit.disabled = true;
      const done = (ok) => {
        status.classList.add("is-visible");
        status.classList.toggle("is-error", !ok);
        $(".status-text", status).innerHTML = ok
          ? `<strong>Danke – Ihre Anfrage ist bei uns.</strong><br>Wir melden uns persönlich mit Verfügbarkeit und Preis.${isDemo ? " <em>(Demo-Modus)</em>" : ""}`
          : `<strong>Das hat leider nicht geklappt.</strong><br>Rufen Sie uns gern direkt an: <a href="tel:+49936099183">09360 99183</a>`;
        submit.disabled = false;
        if (ok) form.querySelectorAll("input:not([type=hidden]):not([type=checkbox]), textarea").forEach((el) => (el.value = ""));
      };
      if (isDemo) return setTimeout(() => done(true), 700);
      try {
        const res = await fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams(new FormData(form)).toString(),
        });
        done(res.ok);
      } catch (_) {
        done(false);
      }
    });
  });

  /* ---------- Kopieren & Teilen ---------- */
  $$("[data-copy]").forEach((el) =>
    el.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(el.dataset.copy);
        showToast(el.dataset.toast || "Kopiert");
      } catch (_) {
        showToast(el.dataset.copy);
      }
    })
  );
  $$("[data-share]").forEach((el) =>
    el.addEventListener("click", async () => {
      const data = { title: document.title, url: location.href };
      if (navigator.share) {
        try {
          await navigator.share(data);
        } catch (_) {}
      } else {
        try {
          await navigator.clipboard.writeText(location.href);
          showToast("Link kopiert");
        } catch (_) {}
      }
    })
  );

  /* ---------- Horizontaler Scroller ---------- */
  $$("[data-scroller]").forEach((wrap) => {
    const track = document.getElementById(wrap.dataset.scroller);
    const [prev, next] = $$("button", wrap);
    if (!track || !prev || !next) return;
    const step = () => (track.firstElementChild ? track.firstElementChild.offsetWidth + 18 : 300);
    const sync = () => {
      prev.disabled = track.scrollLeft < 8;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 8;
    };
    prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));
    next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
    track.addEventListener("scroll", sync, { passive: true });
    addEventListener("resize", sync);
    sync();
  });

  /* ---------- Galerie-Lightbox ---------- */
  const lb = $(".lightbox");
  const gallery = $("[data-gallery]");
  if (lb && gallery) {
    const slides = $$("[data-slide]", gallery).map((b) => {
      const ph = $(".ph", b);
      return { cls: ph.className, label: ph.getAttribute("aria-label") || "" };
    });
    const stage = $(".lb-stage", lb);
    const counter = $(".lb-count", lb);
    let i = 0;
    const show = (n) => {
      i = (n + slides.length) % slides.length;
      const s = slides[i];
      stage.innerHTML = `<div class="${s.cls}" role="img" aria-label="${s.label}"><span class="ph-label">${s.label}</span></div>`;
      counter.textContent = `${i + 1} / ${slides.length}`;
    };
    const open = (n) => {
      show(n);
      lb.showModal();
    };
    $$("[data-slide]", gallery).forEach((b, n) => b.addEventListener("click", () => open(n)));
    $$("[data-open-gallery]").forEach((b) => b.addEventListener("click", () => open(0)));
    $("[data-lb-prev]", lb).addEventListener("click", () => show(i - 1));
    $("[data-lb-next]", lb).addEventListener("click", () => show(i + 1));
    $("[data-lb-close]", lb).addEventListener("click", () => lb.close());
    lb.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(i - 1);
      if (e.key === "ArrowRight") show(i + 1);
    });
    let x0 = null;
    stage.addEventListener("pointerdown", (e) => (x0 = e.clientX));
    stage.addEventListener("pointerup", (e) => {
      if (x0 === null) return;
      const dx = e.clientX - x0;
      if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  }

  /* ---------- Mobile Buchungsleiste (Detailseite) ---------- */
  const mobileBook = $(".mobile-book");
  const bookCard = $("[data-book-card]");
  if (mobileBook && bookCard && "IntersectionObserver" in window) {
    let cardVisible = false;
    new IntersectionObserver(([en]) => {
      cardVisible = en.isIntersecting;
      sync();
    }).observe(bookCard);
    const sync = () => mobileBook.classList.toggle("is-visible", scrollY > 500 && !cardVisible);
    addEventListener("scroll", sync, { passive: true });
  }

  /* ---------- Jahr im Footer ---------- */
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
})();
