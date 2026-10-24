/* Ferienwohnungen Voll – Interaktionen (ohne Framework, progressive enhancement) */
(() => {
  const root = document.documentElement;
  root.classList.remove("no-js");
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const store = {
    get(k, d) { try { const v = sessionStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (_) { return d; } },
    set(k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (_) {} },
    getL(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (_) { return d; } },
    setL(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (_) {} },
  };

  /* ---------- Header ---------- */
  const header = $(".site-header");
  const onScroll = () => header && header.classList.toggle("is-scrolled", scrollY > 4);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  const menuBtn = $("[data-menu]");
  const menuPop = $(".menu-pop");
  if (menuBtn && menuPop) {
    const set = (open) => { menuBtn.setAttribute("aria-expanded", String(open)); menuPop.classList.toggle("is-open", open); };
    menuBtn.addEventListener("click", (e) => { e.stopPropagation(); set(!menuPop.classList.contains("is-open")); });
    document.addEventListener("click", (e) => { if (!menuPop.contains(e.target)) set(false); });
    $$("a", menuPop).forEach((a) => a.addEventListener("click", () => set(false)));
  }

  /* ---------- Bilder: sanft einblenden, fehlende Fotos → Platzhalter ---------- */
  $$(".media img").forEach((img) => {
    const media = img.closest(".media");
    if (img.complete) {
      if (!img.naturalWidth) media.classList.add("is-missing");
      return;
    }
    img.classList.add("is-loading");
    img.addEventListener("load", () => img.classList.remove("is-loading"), { once: true });
    img.addEventListener("error", () => media.classList.add("is-missing"), { once: true });
  });

  /* ---------- Reveal ---------- */
  const reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
    }), { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
    reveals.forEach((el) => io.observe(el));
  } else reveals.forEach((el) => el.classList.add("is-in"));

  /* ---------- Toast ---------- */
  const toast = $(".toast");
  let toastT;
  const showToast = (msg) => {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("is-visible");
    clearTimeout(toastT);
    toastT = setTimeout(() => toast.classList.remove("is-visible"), 2200);
  };

  /* ---------- Foto-Slider (Wischen, Ziehen mit der Maus nach 21st.dev „Image Swiper“) ---------- */
  $$("[data-slider]").forEach((slider) => {
    const track = $(".slider-track", slider);
    const prev = $(".slider-btn.prev", slider);
    const next = $(".slider-btn.next", slider);
    const dots = $$(".dots i", slider);
    const counter = $(".slider-count", slider);
    const extCount = $(".gallery-count", slider.parentElement);
    const n = track.children.length;
    const idx = () => Math.round(track.scrollLeft / track.clientWidth);
    const sync = () => {
      const i = idx();
      dots.forEach((d, k) => d.classList.toggle("on", k === i));
      if (prev) prev.disabled = i <= 0;
      if (next) next.disabled = i >= n - 1;
      if (counter) counter.textContent = `${i + 1} / ${n}`;
      if (extCount) extCount.textContent = `${i + 1} / ${n}`;
    };
    const goTo = (i) => track.scrollTo({ left: Math.max(0, Math.min(n - 1, i)) * track.clientWidth, behavior: reduceMotion ? "auto" : "smooth" });
    const step = (d) => (e) => { e.preventDefault(); e.stopPropagation(); goTo(idx() + d); };
    prev && prev.addEventListener("click", step(-1));
    next && next.addEventListener("click", step(1));
    track.addEventListener("scroll", () => requestAnimationFrame(sync), { passive: true });

    /* Maus: ziehen wie auf dem Handy; ab 10 px Weg wird geblättert */
    let start = null, moved = 0;
    track.addEventListener("pointerdown", (e) => {
      if (e.pointerType !== "mouse" || e.button !== 0) return;
      start = { x: e.clientX, left: track.scrollLeft, i: idx() };
      moved = 0;
    });
    addEventListener("pointermove", (e) => {
      if (!start) return;
      moved = e.clientX - start.x;
      if (Math.abs(moved) > 3) slider.classList.add("is-dragging");
      track.scrollLeft = start.left - moved;
    });
    addEventListener("pointerup", () => {
      if (!start) return;
      const from = start.i;
      start = null;
      slider.classList.remove("is-dragging");
      goTo(moved <= -10 ? from + 1 : moved >= 10 ? from - 1 : from);
    });
    /* Klick aufs Foto öffnet die Wohnung (außer nach dem Ziehen) */
    const cover = slider.closest(".listing") && $("a.cover", slider.closest(".listing"));
    track.addEventListener("click", (e) => {
      if (Math.abs(moved) > 3) { e.preventDefault(); moved = 0; return; }
      if (cover) cover.click();
    });
    sync();
  });

  /* ---------- Bewertungen: Snap-Slider mit Punkten (nach 21st.dev „Testimonials Section“) ---------- */
  $$("[data-rv]").forEach((track) => {
    const wrap = track.parentElement;
    const nav = $(".rv-nav", wrap);
    const dotsEl = $("[data-rv-dots]", wrap);
    const count = track.children.length;
    let pages = 1;
    const page = () => {
      const card = track.firstElementChild;
      const per = Math.max(1, Math.round(track.clientWidth / Math.max(1, card ? card.offsetWidth : track.clientWidth)));
      pages = Math.max(1, Math.ceil(count / per));
      return Math.min(pages - 1, Math.max(0, Math.round(track.scrollLeft / Math.max(1, track.clientWidth - 1))));
    };
    const render = () => {
      const i = page();
      nav.hidden = pages <= 1;
      if (dotsEl.children.length !== pages) {
        dotsEl.innerHTML = Array.from({ length: pages }, (_, k) => `<button type="button" aria-label="Seite ${k + 1}"></button>`).join("");
        $$("button", dotsEl).forEach((b, k) => b.addEventListener("click", () => track.scrollTo({ left: k * track.clientWidth })));
      }
      $$("button", dotsEl).forEach((b, k) => b.setAttribute("aria-current", String(k === i)));
    };
    const turn = (dir) => {
      const max = track.scrollWidth - track.clientWidth;
      if (dir > 0 && track.scrollLeft >= max - 4) track.scrollTo({ left: 0 });
      else if (dir < 0 && track.scrollLeft <= 4) track.scrollTo({ left: max });
      else track.scrollBy({ left: dir * track.clientWidth });
    };
    $("[data-rv-prev]", wrap).addEventListener("click", () => turn(-1));
    $("[data-rv-next]", wrap).addEventListener("click", () => turn(1));
    track.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") { e.preventDefault(); turn(e.key === "ArrowRight" ? 1 : -1); }
    });
    track.addEventListener("scroll", () => requestAnimationFrame(render), { passive: true });
    if ("ResizeObserver" in window) new ResizeObserver(render).observe(track);
    render();
  });

  /* ---------- Merken (Herz) ---------- */
  const saved = new Set(store.getL("fewo-saved", []));
  $$("[data-save]").forEach((btn) => {
    const id = btn.dataset.save;
    btn.setAttribute("aria-pressed", String(saved.has(id)));
    btn.addEventListener("click", (e) => {
      e.preventDefault(); e.stopPropagation();
      saved.has(id) ? saved.delete(id) : saved.add(id);
      const on = saved.has(id);
      btn.setAttribute("aria-pressed", String(on));
      store.setL("fewo-saved", [...saved]);
      showToast(on ? "Gemerkt" : "Aus Merkliste entfernt");
    });
  });

  /* ---------- Filter ---------- */
  const chips = $$("[data-filter]");
  const listings = $$("[data-tags]");
  const countEl = $("[data-filter-count]");
  const applyFilter = (f) => {
    let shown = 0;
    listings.forEach((l) => {
      const ok = f === "alle" || l.dataset.tags.split(" ").includes(f);
      if (ok) {
        if (l.hidden) { l.hidden = false; l.classList.remove("is-entering"); void l.offsetWidth; l.classList.add("is-entering"); }
        if (l.classList.contains("listing")) shown++;
      } else l.hidden = true;
    });
    chips.forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.filter === f)));
    if (countEl) countEl.textContent = f === "alle" ? "" : `${shown} ${shown === 1 ? "Unterkunft" : "Unterkünfte"}`;
  };
  chips.forEach((c) => c.addEventListener("click", () => applyFilter(c.dataset.filter)));
  $$("[data-filter-link]").forEach((a) => a.addEventListener("click", () => applyFilter(a.dataset.filterLink)));

  /* ==========================================================================
     Buchungszustand: Zeitraum + Gäste (geteilt von Suche, Kalender, Karte, Formular)
     ========================================================================== */
  const maxGuests = Number(document.body.dataset.maxGuests || 6);
  const state = Object.assign({ start: null, end: null, adults: 2, children: 0, infants: 0, place: "" }, store.get("fewo-booking", {}));
  const subs = new Set();
  const emit = () => { store.set("fewo-booking", state); subs.forEach((fn) => fn(state)); };
  const setState = (patch) => { Object.assign(state, patch); emit(); };

  const D = (s) => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const today = new Date(); today.setHours(0, 0, 0, 0);
  if (state.start && D(state.start) < today) Object.assign(state, { start: null, end: null });
  /* Gästezahl an die Wohnung anpassen (z. B. 6 aus der Suche → max. 4 in Würzburg) */
  while (state.adults + state.children > maxGuests) state.children > 0 ? state.children-- : state.adults--;
  const fmtShort = new Intl.DateTimeFormat("de-DE", { day: "numeric", month: "short" });
  const fmtMonth = new Intl.DateTimeFormat("de-DE", { month: "long", year: "numeric" });
  const nights = () => (state.start && state.end ? Math.round((D(state.end) - D(state.start)) / 864e5) : 0);
  const guestsTotal = () => state.adults + state.children;
  const guestsLabel = () => {
    const g = guestsTotal();
    let s = `${g} ${g === 1 ? "Gast" : "Gäste"}`;
    if (state.infants) s += `, ${state.infants} ${state.infants === 1 ? "Kleinkind" : "Kleinkinder"}`;
    return s;
  };

  /* Anzeigen aktualisieren */
  subs.add(() => {
    $$("[data-show]").forEach((el) => {
      const k = el.dataset.show;
      let v = "", set = true;
      if (k === "start") v = state.start ? fmtShort.format(D(state.start)) : (set = false, el.dataset.empty || "Datum");
      if (k === "end") v = state.end ? fmtShort.format(D(state.end)) : (set = false, el.dataset.empty || "Datum");
      if (k === "guests") v = guestsLabel();
      if (k === "range") v = state.start && state.end ? `${fmtShort.format(D(state.start))} – ${fmtShort.format(D(state.end))}` : (set = false, el.dataset.empty || "Zeitraum wählen");
      if (k === "nights") { const n = nights(); v = n ? `${n} ${n === 1 ? "Nacht" : "Nächte"}` : (set = false, el.dataset.empty || ""); }
      if (k === "place") v = state.place === "wuerzburg" ? "Würzburg · Altstadt" : state.place === "thuengen" ? "Thüngen · Schlossberg" : (set = false, el.dataset.empty || "Würzburg oder Thüngen");
      el.textContent = v;
      el.classList.toggle("is-set", set);
    });
    $$("[data-bind]").forEach((inp) => {
      const k = inp.dataset.bind;
      const v = k === "guests" ? guestsLabel() : state[k] || "";
      if (inp.value !== v) inp.value = v;
    });
    $$("[data-guest]").forEach((st) => {
      const k = st.dataset.guest;
      const out = $("output", st);
      const [minus, plus] = $$("button", st);
      if (out.textContent !== String(state[k])) {
        out.textContent = state[k];
        out.classList.remove("bump"); void out.offsetWidth; out.classList.add("bump");
      }
      const min = k === "adults" ? 1 : 0;
      minus.disabled = state[k] <= min;
      plus.disabled = k === "infants" ? state[k] >= 2 : guestsTotal() >= maxGuests;
    });
    $$("[data-requires-dates]").forEach((el) => (el.hidden = !(state.start && state.end)));
  });

  /* Gäste-Stepper */
  $$("[data-guest]").forEach((st) => {
    const k = st.dataset.guest;
    const [minus, plus] = $$("button", st);
    minus.addEventListener("click", () => setState({ [k]: Math.max(k === "adults" ? 1 : 0, state[k] - 1) }));
    plus.addEventListener("click", () => setState({ [k]: state[k] + 1 }));
  });

  /* Native Datumsfelder im Anfrageformular ↔ Zustand */
  $$("input[type=date][data-bind]").forEach((inp) => {
    inp.min = iso(today);
    inp.addEventListener("change", () => {
      const patch = { [inp.dataset.bind]: inp.value || null };
      if (inp.dataset.bind === "start" && state.end && inp.value && inp.value >= state.end) patch.end = null;
      setState(patch);
    });
  });
  $$("select[data-place]").forEach((sel) => sel.addEventListener("change", () => setState({ place: sel.value })));

  /* ---------- Kalender ---------- */
  const DOW = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
  const calendars = [];
  function Calendar(el) {
    let offset = 0;
    let hover = null;
    const two = el.classList.contains("two");
    const render = () => {
      const base = new Date(today.getFullYear(), today.getMonth() + offset, 1);
      const months = [0, 1].map((m) => new Date(base.getFullYear(), base.getMonth() + m, 1));
      const s = state.start, e = state.end;
      const previewEnd = s && !e && hover && hover > s ? hover : null;
      el.innerHTML = `
        <div class="cal-nav">
          <button type="button" data-cal-prev aria-label="Vorheriger Monat" ${offset <= 0 ? "disabled" : ""}><svg width="16" height="16"><use href="#i-left"/></svg></button>
          <button type="button" data-cal-next aria-label="Nächster Monat" ${offset >= 16 ? "disabled" : ""}><svg width="16" height="16"><use href="#i-right"/></svg></button>
        </div>
        <div class="cal-months">${months.map((m) => {
          const first = (m.getDay() + 6) % 7;
          const days = new Date(m.getFullYear(), m.getMonth() + 1, 0).getDate();
          let cells = DOW.map((d) => `<div class="cal-dow">${d}</div>`).join("") + "<div></div>".repeat(first);
          for (let d = 1; d <= days; d++) {
            const date = new Date(m.getFullYear(), m.getMonth(), d);
            const id = iso(date);
            const cls = ["cal-day"];
            if (date.getTime() === today.getTime()) cls.push("today");
            if (s === id) cls.push("start");
            if (e === id) cls.push("end");
            if (s && e) cls.push("has-end");
            if (s && e && id > s && id < e) cls.push("in-range");
            if (previewEnd && id > s && id <= previewEnd) cls.push(id === previewEnd ? "preview" : "in-range");
            const past = date < today;
            cells += `<div class="${cls.join(" ")}"><button type="button" data-day="${id}" ${past ? "disabled" : ""} aria-label="${new Intl.DateTimeFormat("de-DE", { dateStyle: "full" }).format(date)}" aria-pressed="${s === id || e === id}">${d}</button></div>`;
          }
          return `<div class="cal-month"><h4>${fmtMonth.format(m)}</h4><div class="cal-grid">${cells}</div></div>`;
        }).join("")}</div>`;
    };
    el.addEventListener("click", (ev) => {
      const b = ev.target.closest("button");
      if (!b || b.disabled) return;
      ev.stopPropagation();
      if (b.hasAttribute("data-cal-prev")) { offset = Math.max(0, offset - (two && innerWidth >= 720 ? 1 : 1)); return render(); }
      if (b.hasAttribute("data-cal-next")) { offset++; return render(); }
      const id = b.dataset.day;
      if (!state.start || state.end || id <= state.start) setState({ start: id, end: null });
      else {
        setState({ end: id });
        el.dispatchEvent(new CustomEvent("range-complete", { bubbles: true }));
      }
    });
    el.addEventListener("mouseover", (ev) => {
      const b = ev.target.closest("[data-day]");
      const v = b ? b.dataset.day : null;
      if (state.start && !state.end && v !== hover) { hover = v; render(); }
    });
    el.addEventListener("mouseleave", () => { if (hover) { hover = null; render(); } });
    calendars.push(render);
    render();
  }
  $$("[data-cal]").forEach((el) => Calendar(el));
  subs.add(() => calendars.forEach((r) => r()));

  /* ---------- Popover & Bottom-Sheet ---------- */
  let openPop = null;
  const closeAll = () => {
    $$(".popover.is-open, .sheet.is-open").forEach((p) => p.classList.remove("is-open"));
    $$("[data-open].is-active").forEach((t) => t.classList.remove("is-active"));
    openPop = null;
  };
  const isHidden = (el) => !el || getComputedStyle(el).display === "none";
  const open = (trigger) => {
    const pop = document.getElementById(trigger.dataset.open);
    const sheet = document.getElementById(trigger.dataset.sheet);
    const target = isHidden(pop) ? sheet : pop;
    if (!target) return;
    const already = target.classList.contains("is-open") && $$("[data-open].is-active").includes(trigger);
    closeAll();
    if (already) return;
    target.classList.add("is-open");
    if (target === pop) trigger.classList.add("is-active");
    openPop = target;
  };
  $$("[data-open]").forEach((t) => t.addEventListener("click", (e) => { e.preventDefault(); e.stopPropagation(); open(t); }));
  $$(".popover").forEach((p) => p.addEventListener("click", (e) => e.stopPropagation()));
  document.addEventListener("click", (e) => { if (openPop && !openPop.contains(e.target) && !e.target.closest(".sheet-panel")) closeAll(); });
  addEventListener("keydown", (e) => e.key === "Escape" && closeAll());
  $$(".sheet").forEach((sh) => sh.addEventListener("click", (e) => { if (e.target === sh) closeAll(); }));
  $$("[data-close]").forEach((b) => b.addEventListener("click", (e) => { e.preventDefault(); closeAll(); }));
  $$("[data-clear-dates]").forEach((b) => b.addEventListener("click", (e) => { e.preventDefault(); e.stopPropagation(); setState({ start: null, end: null }); }));
  /* Nach Abreise-Wahl: in der Suche weiter zu Gästen, sonst schließen */
  document.addEventListener("range-complete", (e) => {
    const next = e.target.closest("[data-after-range]");
    setTimeout(() => {
      if (next && !isHidden(document.getElementById(next.dataset.afterRange))) {
        const t = $(`[data-open="${next.dataset.afterRange}"]`);
        t ? open(t) : closeAll();
      } else if (e.target.closest(".popover")) closeAll();
    }, 260);
  });

  /* ---------- Startseite: Suche → Anfrageformular ---------- */
  const search = $("[data-search]");
  if (search) {
    search.addEventListener("submit", (e) => {
      e.preventDefault();
      closeAll();
      const sel = $("#anfrage-form select[name=wohnung]");
      if (sel && state.place) sel.value = state.place === "wuerzburg" ? "Würzburg – egal welche" : "Thüngen – egal welche";
      const target = document.getElementById("anfrage");
      target && target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
      setTimeout(() => { const n = $("#anfrage-form [name=name]"); n && n.focus({ preventScroll: true }); }, 700);
    });
  }
  $$("[data-unit]").forEach((a) => a.addEventListener("click", () => {
    const sel = $("#anfrage-form select[name=wohnung]");
    if (sel) sel.value = a.dataset.unit;
  }));

  /* ---------- Detailseite: Buchungskarte ---------- */
  $$("[data-book]").forEach((form) => {
    const more = $(".book-more", form);
    const btn = $("[data-book-next]", form);
    btn.addEventListener("click", (e) => {
      if (!state.start || !state.end) { e.preventDefault(); const t = $("[data-open][data-sheet='sheet-cal']", form) || $("[data-open]", form); t && open(t); return; }
      if (!more.classList.contains("is-open")) {
        e.preventDefault();
        more.classList.add("is-open");
        more.removeAttribute("inert");
        $(".btn-label", btn).textContent = "Anfrage senden";
        setTimeout(() => $("input:not([type=hidden])", more).focus({ preventScroll: true }), 350);
      }
    });
  });

  /* ---------- Formulare (Netlify Forms, lokal Demo-Modus) ---------- */
  const isDemo = location.protocol === "file:" || /^(localhost|127\.|0\.0\.0\.0)/.test(location.hostname);
  $$("form[data-inquiry]").forEach((form) => {
    const status = $(".form-status", form);
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const more = $(".book-more", form);
      if (more && !more.classList.contains("is-open")) return;
      if (!form.reportValidity()) return;
      const submit = $("button[type=submit]", form);
      submit.disabled = true;
      const done = (ok) => {
        status.classList.add("is-visible");
        status.classList.toggle("is-error", !ok);
        $(".status-text", status).innerHTML = ok
          ? `<strong>Danke – Ihre Anfrage ist bei uns.</strong><br>Wir melden uns persönlich mit Verfügbarkeit und Preis.${isDemo ? " <em>(Demo)</em>" : ""}`
          : `<strong>Das hat leider nicht geklappt.</strong><br>Rufen Sie uns gern an: <a class="u-link" href="tel:+49936099183">09360 99183</a>`;
        submit.disabled = false;
        if (ok) $$("input[name=name], input[name=email], textarea", form).forEach((el) => (el.value = ""));
      };
      if (isDemo) return setTimeout(() => done(true), 600);
      try {
        const res = await fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams(new FormData(form)).toString() });
        done(res.ok);
      } catch (_) { done(false); }
    });
  });

  /* ---------- Mehr lesen, Ausstattung ---------- */
  $$("[data-readmore]").forEach((btn) => {
    const box = document.getElementById(btn.dataset.readmore);
    btn.addEventListener("click", () => {
      const openNow = box.classList.toggle("is-open");
      $("span", btn).textContent = openNow ? "Weniger anzeigen" : "Mehr anzeigen";
    });
  });
  $$("[data-amenities]").forEach((btn) => {
    const list = document.getElementById(btn.dataset.amenities);
    const label = btn.textContent;
    btn.addEventListener("click", () => {
      const all = list.classList.toggle("is-all");
      btn.textContent = all ? "Weniger anzeigen" : label;
    });
  });

  /* ---------- Kopieren & Teilen ---------- */
  $$("[data-copy]").forEach((el) => el.addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(el.dataset.copy); showToast(el.dataset.toast || "Kopiert"); } catch (_) { showToast(el.dataset.copy); }
  }));
  $$("[data-share]").forEach((el) => el.addEventListener("click", async () => {
    if (navigator.share) { try { await navigator.share({ title: document.title, url: location.href }); } catch (_) {} return; }
    try { await navigator.clipboard.writeText(location.href); showToast("Link kopiert"); } catch (_) {}
  }));

  /* ---------- Lightbox ---------- */
  const lb = $(".lightbox");
  if (lb) {
    const photos = JSON.parse(lb.dataset.photos || "[]");
    const img = $(".lb-stage img", lb);
    const cap = $(".lb-caption", lb);
    const cnt = $(".lb-count", lb);
    let i = 0;
    const show = (n) => {
      i = (n + photos.length) % photos.length;
      img.style.animation = "none"; void img.offsetWidth; img.style.animation = "";
      img.src = photos[i].src;
      img.alt = photos[i].alt;
      cap.textContent = photos[i].alt;
      cnt.textContent = `${i + 1} / ${photos.length}`;
    };
    $$("[data-photo]").forEach((b) => b.addEventListener("click", () => { show(Number(b.dataset.photo)); lb.showModal(); }));
    $("[data-lb-prev]", lb).addEventListener("click", () => show(i - 1));
    $("[data-lb-next]", lb).addEventListener("click", () => show(i + 1));
    $("[data-lb-close]", lb).addEventListener("click", () => lb.close());
    lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
    let x0 = null;
    img.addEventListener("pointerdown", (e) => (x0 = e.clientX));
    img.addEventListener("pointerup", (e) => { if (x0 !== null && Math.abs(e.clientX - x0) > 40) show(i + (e.clientX < x0 ? 1 : -1)); x0 = null; });
  }

  /* ---------- Region-Scroller ---------- */
  $$("[data-scroller]").forEach((nav) => {
    const track = document.getElementById(nav.dataset.scroller);
    const [prev, next] = $$("button", nav);
    const step = () => (track.firstElementChild ? track.firstElementChild.offsetWidth + 20 : 300);
    const sync = () => { prev.disabled = track.scrollLeft < 8; next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 8; };
    prev.addEventListener("click", () => track.scrollBy({ left: -step(), behavior: "smooth" }));
    next.addEventListener("click", () => track.scrollBy({ left: step(), behavior: "smooth" }));
    track.addEventListener("scroll", sync, { passive: true });
    addEventListener("resize", sync);
    sync();
  });

  /* ---------- Bildnachweise (vom Build erzeugt) ---------- */
  const credits = $("[data-credits]");
  if (credits) {
    fetch(credits.dataset.credits).then((r) => (r.ok ? r.json() : Promise.reject())).then((data) => {
      const seen = new Set();
      const items = Object.values(data).filter((c) => !seen.has(c.url) && seen.add(c.url));
      $("ul", credits).insertAdjacentHTML("beforeend", items.map((c) => c.source === "Unsplash"
        ? `<li>Foto · <a href="${c.url}" rel="noopener" target="_blank">Unsplash</a></li>`
        : `<li>${c.title.replace(/\.(jpe?g|png)$/i, "")} · ${c.author || "unbekannt"} · ${c.license || ""} · <a href="${c.url}" rel="noopener" target="_blank">Wikimedia Commons</a></li>`).join(""));
    }).catch(() => {});
  }

  /* ---------- Jahr ---------- */
  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

  emit();
})();
