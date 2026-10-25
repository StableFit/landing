/*
 * Deep-link pages served through 404.html (GitHub Pages has no server routing).
 *
 *   /app/<screen>[?promo=…]  coach app screen (stablefitpro:// scheme); laptop -> QR + stores
 *   /join/<code>              client sign-up with the registration code (stablefit:// scheme);
 *                             no app -> code + the right store for the device
 *   /i/<token>[/viber]        invite text for the coach to forward (copy, Telegram, WhatsApp, Viber)
 *   /c/<code>                 promo code -> coach paywall with the code prefilled
 *
 * Texts: uk / en by ?lang=, else the browser language (uk / ru -> uk).
 * Deep links are the apps' own schemes: the prod apps have no Universal Links
 * yet, so on a phone we try the scheme and fall back to the store after 1.5 s.
 */
(function () {
  "use strict";

  var SITE = "https://stable-fit.com";
  var INVITE_API = {
    prod: "https://iqgixbirxzmprdaozwio.supabase.co/functions/v1/invite-info",
    dev: "https://bvzkpfbirwpkgyvnufji.supabase.co/functions/v1/invite-info"
  };
  var STORES = {
    coach: {
      ios: "https://apps.apple.com/app/id6755842178",
      android: "https://play.google.com/store/apps/details?id=com.fit.stable.pro"
    },
    client: {
      ios: "https://apps.apple.com/app/id6755842057",
      android: "https://play.google.com/store/apps/details?id=com.fit.stable.app"
    }
  };
  var COACH_SCHEME = "stablefitpro://stablefitpro.com";
  var CLIENT_SCHEME = "stablefit://stablefit.com";

  // Coach app screens reachable by URL (prod, origin/main). Anything else -> clients list.
  var APP_SCREENS = {
    "clients/new": { path: "/createClient", hint: "app.hint.createClient" },
    "clients": { path: "/clients", hint: "app.hint.clients" },
    "chats": { path: "/chats", hint: "app.hint.chats" },
    "settings/notifications": { path: "/notificationSettings", hint: "app.hint.notifications" },
    "paywall": { path: "/payWallPage", hint: "app.hint.paywall", query: { promo: "promocode" } }
  };

  var T = {
    uk: {
      "app.title": "Відкрий StableFit Pro на телефоні",
      "app.lead": "Наведи камеру телефону на код - відкриється потрібний екран, а без застосунку - магазин.",
      "app.opening": "Відкриваємо StableFit Pro…",
      "app.notOpened": "Натисни кнопку - відкриється StableFit Pro, а якщо його ще немає, магазин.",
      "app.open": "Відкрити StableFit Pro",
      "app.hint.createClient": "Екран «Додати клієнта»",
      "app.hint.clients": "Список клієнтів",
      "app.hint.chats": "Чати",
      "app.hint.notifications": "Налаштування сповіщень",
      "app.hint.paywall": "Екран StableFit PRO з промокодом",
      "join.title": "Твій код для StableFit",
      "join.lead": "Встанови StableFit і введи цей код під час реєстрації - і твій тренер побачить твої заміри, харчування й тренування.",
      "join.opening": "Відкриваємо StableFit…",
      "join.open": "Відкрити або встановити StableFit",
      "join.afterInstall": "Кнопка відкриє StableFit, а якщо його ще немає - магазин. Після встановлення введи код.",
      "join.copy": "Скопіювати код",
      "join.scanHint": "Наведи камеру телефону на код - відкриється застосунок або магазин.",
      "promo.scanHint": "Наведи камеру телефону на код - відкриється StableFit Pro або магазин.",
      "get.scanHint": "Наведи камеру телефону на код - відкриється магазин твого телефону.",
      "invite.title": "Повідомлення для клієнта",
      "invite.lead": "Скопіюй текст і надішли клієнту - або відправ одним натисканням.",
      "invite.copy": "Скопіювати текст",
      "invite.viberLead": "Відкриваємо Viber… Якщо не відкрився - натисни кнопку.",
      "invite.notFound": "Це посилання застаріло. Відкрий картку клієнта у StableFit Pro - там є код і кнопка «Поділитися».",
      "invite.error": "Не вдалося завантажити. Спробуй ще раз за хвилину.",
      "promo.title": "Твій промокод",
      "promo.lead": "Введи його на екрані StableFit PRO - знижка застосується на першу оплату.",
      "promo.copy": "Скопіювати код",
      "promo.open": "Відкрити StableFit Pro",
      "promo.afterInstall": "Кнопка відкриє StableFit Pro з кодом, а якщо застосунку ще немає - магазин.",
      "get.title": "StableFit для клієнтів",
      "get.lead": "Завантаж застосунок - і введи код від свого тренера.",
      "copied": "Скопійовано",
      "copyFailed": "Не вдалося скопіювати - виділи текст вручну",
      "stores.ios": "App Store",
      "stores.android": "Google Play",
      "or": "або",
      "telegram": "Telegram",
      "whatsapp": "WhatsApp",
      "viber": "Viber"
    },
    pl: {
      "app.title": "Otwórz StableFit Pro na telefonie",
      "app.lead": "Skieruj aparat telefonu na kod - otworzy się właściwy ekran, a bez aplikacji - sklep.",
      "app.opening": "Otwieramy StableFit Pro…",
      "app.notOpened": "Naciśnij przycisk - otworzy się StableFit Pro, a jeśli go jeszcze nie ma, sklep.",
      "app.open": "Otwórz StableFit Pro",
      "app.hint.createClient": "Ekran «Dodaj klienta»",
      "app.hint.clients": "Lista klientów",
      "app.hint.chats": "Czaty",
      "app.hint.notifications": "Ustawienia powiadomień",
      "app.hint.paywall": "Ekran StableFit PRO z kodem promocyjnym",
      "join.title": "Twój kod do StableFit",
      "join.lead": "Zainstaluj StableFit i wpisz ten kod przy rejestracji - twój trener zobaczy twoje pomiary, posiłki i treningi.",
      "join.opening": "Otwieramy StableFit…",
      "join.open": "Otwórz lub zainstaluj StableFit",
      "join.afterInstall": "Przycisk otworzy StableFit, a jeśli go jeszcze nie ma - sklep. Po instalacji wpisz kod.",
      "join.copy": "Skopiuj kod",
      "join.scanHint": "Skieruj aparat telefonu na kod - otworzy się aplikacja albo sklep.",
      "promo.scanHint": "Skieruj aparat telefonu na kod - otworzy się StableFit Pro albo sklep.",
      "get.scanHint": "Skieruj aparat telefonu na kod - otworzy się sklep twojego telefonu.",
      "invite.title": "Wiadomość dla klienta",
      "invite.lead": "Skopiuj tekst i wyślij klientowi - albo wyślij jednym kliknięciem.",
      "invite.copy": "Skopiuj tekst",
      "invite.viberLead": "Otwieramy Viber… Jeśli się nie otworzył, naciśnij przycisk.",
      "invite.notFound": "Ten link wygasł. Otwórz kartę klienta w StableFit Pro - jest tam kod i przycisk «Udostępnij».",
      "invite.error": "Nie udało się wczytać. Spróbuj ponownie za minutę.",
      "promo.title": "Twój kod promocyjny",
      "promo.lead": "Wpisz go na ekranie StableFit PRO - zniżka obejmie pierwszą płatność.",
      "promo.copy": "Skopiuj kod",
      "promo.open": "Otwórz StableFit Pro",
      "promo.afterInstall": "Przycisk otworzy StableFit Pro z kodem, a jeśli aplikacji jeszcze nie ma - sklep.",
      "get.title": "StableFit dla klientów",
      "get.lead": "Zainstaluj aplikację i wpisz kod od swojego trenera.",
      "copied": "Skopiowano",
      "copyFailed": "Nie udało się skopiować - zaznacz tekst ręcznie",
      "stores.ios": "App Store",
      "stores.android": "Google Play",
      "or": "lub",
      "telegram": "Telegram",
      "whatsapp": "WhatsApp",
      "viber": "Viber"
    },
    en: {
      "app.title": "Open StableFit Pro on your phone",
      "app.lead": "Point your phone camera at the code - the right screen opens, or the store if the app is missing.",
      "app.opening": "Opening StableFit Pro…",
      "app.notOpened": "Tap the button - StableFit Pro opens, or the store if it is not installed yet.",
      "app.open": "Open StableFit Pro",
      "app.hint.createClient": "The «Add client» screen",
      "app.hint.clients": "Clients list",
      "app.hint.chats": "Chats",
      "app.hint.notifications": "Notification settings",
      "app.hint.paywall": "The StableFit PRO screen with your promo code",
      "join.title": "Your StableFit code",
      "join.lead": "Install StableFit and enter this code when you sign up - your coach will see your measurements, nutrition and workouts.",
      "join.opening": "Opening StableFit…",
      "join.open": "Open or install StableFit",
      "join.afterInstall": "The button opens StableFit, or the store if it is not installed yet. After installing, enter the code.",
      "join.copy": "Copy code",
      "join.scanHint": "Point your phone camera at the code - the app or the store opens.",
      "promo.scanHint": "Point your phone camera at the code - StableFit Pro or the store opens.",
      "get.scanHint": "Point your phone camera at the code - your phone's store opens.",
      "invite.title": "Message for your client",
      "invite.lead": "Copy the text and send it to your client - or send it in one tap.",
      "invite.copy": "Copy text",
      "invite.viberLead": "Opening Viber… If it did not open, tap the button.",
      "invite.notFound": "This link has expired. Open the client card in StableFit Pro - the code and the share button are there.",
      "invite.error": "Could not load. Try again in a minute.",
      "promo.title": "Your promo code",
      "promo.lead": "Enter it on the StableFit PRO screen - the discount applies to your first payment.",
      "promo.copy": "Copy code",
      "promo.open": "Open StableFit Pro",
      "promo.afterInstall": "The button opens StableFit Pro with the code, or the store if it is not installed yet.",
      "get.title": "StableFit for clients",
      "get.lead": "Install the app and enter the code from your coach.",
      "copied": "Copied",
      "copyFailed": "Could not copy - select the text by hand",
      "stores.ios": "App Store",
      "stores.android": "Google Play",
      "or": "or",
      "telegram": "Telegram",
      "whatsapp": "WhatsApp",
      "viber": "Viber"
    }
  };

  var params = new URLSearchParams(location.search);
  var lang = pickLang();
  var ua = navigator.userAgent || "";
  var isIOS = /iPhone|iPad|iPod/i.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  var isAndroid = /Android/i.test(ua);
  var isPhone = isIOS || isAndroid;

  // Same choice as the site header (script/main.js sets <html data-sf-lang>):
  // ?lang=, else the language picked before, else the browser.
  function pickLang() {
    var site = document.documentElement.getAttribute("data-sf-lang");
    var q = (params.get("lang") || site || "").toLowerCase();
    if (q === "ua" || q === "uk") return "uk";
    if (q === "en" || q === "pl") return q;
    var nav = ((navigator.languages && navigator.languages[0]) || navigator.language || "uk").toLowerCase();
    if (/^(uk|ru)/.test(nav)) return "uk";
    return /^pl/.test(nav) ? "pl" : "en";
  }
  function t(key) { return (T[lang] && T[lang][key]) || T.uk[key] || key; }
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else if (k === "html") node.innerHTML = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) node.appendChild(c); });
    return node;
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // ---- building blocks ------------------------------------------------------

  function pill(label, href, opts) {
    opts = opts || {};
    var a = el("a", { class: "dl-pill" + (opts.outline ? " dl-pill-outline" : ""), href: href, text: label });
    if (opts.blank) { a.target = "_blank"; a.rel = "noopener"; }
    if (opts.onClick) a.addEventListener("click", opts.onClick);
    return a;
  }
  function storeUrl(app) {
    return isIOS ? STORES[app].ios : STORES[app].android;
  }
  // One button on a phone: try the app scheme, and when nothing opened within
  // 1.5 s go to this device's store. The user never picks a platform.
  function openOrInstall(label, app, schemeUrl) {
    return pill(label, schemeUrl, {
      onClick: function (e) {
        e.preventDefault();
        tryOpen(schemeUrl, function () { location.href = storeUrl(app); });
      }
    });
  }
  // Laptop: the QR alone. The phone that scans it lands on this same page and
  // gets the one-button flow above.
  function laptop(url, hintKey) {
    return [qr(url), el("p", { class: "dl-hint", text: t(hintKey) })];
  }
  function qr(url) {
    var box = el("div", { class: "dl-qr", "aria-hidden": "true" });
    if (typeof window.qrcode !== "function") return box;
    try {
      var q = window.qrcode(0, "M");
      q.addData(url);
      q.make();
      box.innerHTML = q.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
    } catch (e) { /* no QR, the buttons still work */ }
    return box;
  }
  function codeBox(code) {
    return el("div", { class: "dl-code", text: code });
  }
  function copyButton(label, text) {
    var btn = el("button", { class: "dl-pill", type: "button", text: label });
    btn.addEventListener("click", function () {
      copyText(text).then(function (ok) {
        btn.textContent = ok ? t("copied") : t("copyFailed");
        setTimeout(function () { btn.textContent = label; }, 2000);
      });
    });
    return btn;
  }
  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).then(function () { return true; }, function () { return legacyCopy(text); });
    }
    return Promise.resolve(legacyCopy(text));
  }
  function legacyCopy(text) {
    var ta = el("textarea", { readonly: "", style: "position:fixed;top:-1000px;opacity:0" });
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    return ok;
  }
  function shareRow(text, url) {
    var enc = encodeURIComponent(text);
    var row = el("div", { class: "dl-share" });
    row.appendChild(pill(t("telegram"), "https://t.me/share/url?url=" + encodeURIComponent(url) + "&text=" + enc, { blank: true }));
    row.appendChild(pill(t("whatsapp"), "https://wa.me/?text=" + enc, { blank: true }));
    row.appendChild(pill(t("viber"), "viber://forward?text=" + enc));
    return row;
  }

  // Try the app scheme on a phone; after 1.5 s without the page going to the
  // background, show the fallback. On a laptop show the fallback right away.
  function tryOpen(schemeUrl, onFallback) {
    if (!isPhone) { onFallback(false); return; }
    var hidden = false;
    var onVis = function () { if (document.hidden) hidden = true; };
    document.addEventListener("visibilitychange", onVis);
    window.addEventListener("pagehide", onVis);
    setTimeout(function () {
      document.removeEventListener("visibilitychange", onVis);
      window.removeEventListener("pagehide", onVis);
      if (!hidden) onFallback(true);
    }, 1500);
    location.href = schemeUrl;
  }

  function render(nodes) {
    var root = document.getElementById("dl-root");
    var legacy = document.getElementById("page-404-content");
    if (legacy) legacy.hidden = true;
    root.innerHTML = "";
    nodes.forEach(function (n) { if (n) root.appendChild(n); });
    root.hidden = false;
    document.body.classList.add("page-deeplink");
  }
  function heading(title, lead) {
    return [
      el("h1", { class: "doc-title dl-title", text: title }),
      lead ? el("p", { class: "doc-lead dl-lead", text: lead }) : null
    ];
  }

  // ---- views ----------------------------------------------------------------

  function viewApp(rest) {
    var key = rest.replace(/\/+$/, "");
    var screen = APP_SCREENS[key] || APP_SCREENS.clients;
    var qs = "";
    if (screen.query) {
      var parts = [];
      Object.keys(screen.query).forEach(function (from) {
        var v = params.get(from);
        if (v) parts.push(screen.query[from] + "=" + encodeURIComponent(v));
      });
      if (parts.length) qs = "?" + parts.join("&");
    }
    var scheme = COACH_SCHEME + screen.path + qs;
    var here = SITE + location.pathname + location.search;
    document.title = t("app.title") + " - StableFit";

    if (!isPhone) {
      render(heading(t("app.title"), t("app.lead")).concat(laptop(here, screen.hint)));
      return;
    }
    render(heading(t("app.opening")));
    tryOpen(scheme, function () {
      render(heading(t("app.title"), t("app.notOpened")).concat([
        el("p", { class: "dl-hint", text: t(screen.hint) }),
        openOrInstall(t("app.open"), "coach", scheme)
      ]));
    });
  }

  function viewJoin(code) {
    code = (code || "").replace(/[^A-Za-z0-9]/g, "").slice(0, 12);
    var scheme = CLIENT_SCHEME + "/createAccount/" + encodeURIComponent(code);
    var here = SITE + "/join/" + code;
    document.title = t("join.title") + " - StableFit";
    var fallback = function () {
      render(heading(t("join.title"), t("join.lead")).concat([
        codeBox(code),
        copyButton(t("join.copy"), code),
        isPhone ? openOrInstall(t("join.open"), "client", scheme) : null
      ]).concat(isPhone ? [el("p", { class: "dl-hint", text: t("join.afterInstall") })] : laptop(here, "join.scanHint")));
    };
    if (!code || !isPhone) { fallback(); return; }
    render(heading(t("join.opening")));
    tryOpen(scheme, fallback);
  }

  function viewInvite(token, viber) {
    token = (token || "").replace(/[^A-Za-z0-9_-]/g, "");
    document.title = t("invite.title") + " - StableFit";
    render(heading(t("invite.title"), "…"));
    var api = INVITE_API[params.get("env") === "dev" ? "dev" : "prod"];
    fetch(api + "?t=" + encodeURIComponent(token), { headers: { accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (d) {
        var text = d.text || "";
        if (viber) {
          location.href = "viber://forward?text=" + encodeURIComponent(text);
          render(heading(t("invite.title"), t("invite.viberLead")).concat([
            pill(t("viber"), "viber://forward?text=" + encodeURIComponent(text)),
            el("pre", { class: "dl-quote", text: text }),
            copyButton(t("invite.copy"), text)
          ]));
          return;
        }
        render(heading(t("invite.title"), t("invite.lead")).concat([
          el("pre", { class: "dl-quote", text: text }),
          copyButton(t("invite.copy"), text),
          shareRow(text, d.share_url || (SITE + "/get"))
        ]));
      })
      .catch(function (status) {
        render(heading(t("invite.title"), status === 404 ? t("invite.notFound") : t("invite.error")));
      });
  }

  function viewPromo(code) {
    code = (code || "").replace(/[^A-Za-z0-9-]/g, "").toUpperCase().slice(0, 32);
    var scheme = COACH_SCHEME + "/payWallPage?promocode=" + encodeURIComponent(code);
    document.title = t("promo.title") + " - StableFit";
    render(heading(t("promo.title"), t("promo.lead")).concat([
      codeBox(code),
      copyButton(t("promo.copy"), code),
      isPhone ? openOrInstall(t("promo.open"), "coach", scheme) : null
    ]).concat(isPhone ? [el("p", { class: "dl-hint", text: t("promo.afterInstall") })] : laptop(SITE + "/c/" + code, "promo.scanHint")));
  }

  function viewGet() {
    document.title = t("get.title") + " - StableFit";
    if (isIOS) { location.replace(STORES.client.ios); return; }
    if (isAndroid) { location.replace(STORES.client.android); return; }
    render(heading(t("get.title"), t("get.lead")).concat(laptop(SITE + "/get", "get.scanHint")));
  }

  // ---- router ---------------------------------------------------------------

  function route() {
    var path = location.pathname.replace(/^\/+/, "");
    var m;
    if ((m = path.match(/^app(?:\/(.*))?$/))) return viewApp(m[1] || "");
    if ((m = path.match(/^join\/([^/]+)\/?$/))) return viewJoin(decodeURIComponent(m[1]));
    if ((m = path.match(/^i\/([^/]+)(\/viber)?\/?$/))) return viewInvite(m[1], Boolean(m[2]));
    if ((m = path.match(/^c\/([^/]+)\/?$/))) return viewPromo(decodeURIComponent(m[1]));
    if (/^get\/?$/.test(path)) return viewGet();
    return false; // plain 404 stays visible
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", route);
  else route();
})();
