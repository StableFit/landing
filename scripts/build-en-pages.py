#!/usr/bin/env python3
"""Generate localized HTML under /en/ and /pl/ from UA sources.

Re-run after editing source HTML or locale files:
  python3 scripts/build-en-pages.py
"""

from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://stable-fit.com"
SCRIPT_VERSION = "20260923"
GENERATED_LANGS = ("en", "pl")

LOCALES = {
    "ua": {
        "html_lang": "uk",
        "hreflang": "uk",
        "og": "uk_UA",
        "schema": "uk-UA",
        "label": "UA",
        "aria": "aria.langUa",
    },
    "en": {
        "html_lang": "en",
        "hreflang": "en",
        "og": "en_US",
        "schema": "en-US",
        "label": "EN",
        "aria": "aria.langEn",
    },
    "pl": {
        "html_lang": "pl",
        "hreflang": "pl",
        "og": "pl_PL",
        "schema": "pl-PL",
        "label": "PL",
        "aria": "aria.langPl",
    },
}

UA_ONLY_SITEMAP = []

BLOG_POST_TITLE_KEYS = {
    "where-to-find-time-to-attract-new-clients": "blog.posts.whereToFindTime.title",
    "why-a-coach-needs-a-system": "blog.posts.whyACoachNeedsASystem.title",
    "free-consultations-and-workouts-ok-or-not": "blog.posts.freeConsultsAndWorkouts.title",
    "should-a-coach-grow-social-media": "blog.posts.shouldACoachGrowSocialMedia.title",
    "why-potential-clients-dont-stay": "blog.posts.whyPotentialClientsDontStay.title",
    "is-coaching-not-for-you": "blog.posts.isCoachingNotForYou.title",
    "secret-principle-of-finding-clients": "blog.posts.secretPrincipleOfFindingClients.title",
    "why-clients-quit-training-even-with-results": "blog.posts.whyClientsQuitEvenWithResults.title",
    "five-autumn-content-topics-for-coaches": "blog.posts.fiveAutumnContentTopics.title",
    "why-coaches-burn-out": "blog.posts.whyCoachesBurnOut.title",
    "official-launch": "blog.posts.officialLaunch.title",
    "five-sales-techniques-for-coaches": "blog.posts.fiveSalesTechniquesForCoaches.title",
    "excel-and-telegram-are-not-a-crm-for-coaches": "blog.posts.excelAndTelegramAreNotACrm.title",
    "crm-for-personal-trainers": "blog.posts.crmForPersonalTrainers.title",
}

FAQ_ITEM_KEYS = (
    "who",
    "excel",
    "clientApp",
    "allInOne",
    "price",
    "notForStudio",
    "platforms",
    "clientPays",
    "invite",
    "online",
    "cancel",
)

PAGES = [
    {
        "src": "index.html",
        "uk": "/",
        "title_key": "coach.meta.title",
        "desc_key": "coach.meta.description",
        "changefreq": "weekly",
        "priority": "1.0",
    },
    {
        "src": "for-clients/index.html",
        "uk": "/for-clients/",
        "title_key": "client.meta.title",
        "desc_key": "client.meta.description",
        "changefreq": "weekly",
        "priority": "0.9",
    },
    {
        "src": "support/index.html",
        "uk": "/support/",
        "title_key": "support.meta.title",
        "desc_key": "support.meta.description",
        "changefreq": "monthly",
        "priority": "0.7",
    },
    {
        "src": "privacy-policy/index.html",
        "uk": "/privacy-policy/",
        "title_key": "privacy.meta.title",
        "desc_key": "privacy.meta.description",
        "changefreq": "yearly",
        "priority": "0.4",
    },
    {
        "src": "terms-and-conditions/index.html",
        "uk": "/terms-and-conditions/",
        "title_key": "terms.meta.title",
        "desc_key": "terms.meta.description",
        "changefreq": "yearly",
        "priority": "0.4",
    },
    {
        "src": "blog/index.html",
        "uk": "/blog/",
        "title_key": "blog.meta.title",
        "desc_key": "blog.meta.description",
        "changefreq": "weekly",
        "priority": "0.6",
    },
    {
        "src": "blog/where-to-find-time-to-attract-new-clients/index.html",
        "uk": "/blog/where-to-find-time-to-attract-new-clients/",
        "title_key": "blog.posts.whereToFindTime.metaTitle",
        "desc_key": "blog.posts.whereToFindTime.description",
        "headline_key": "blog.posts.whereToFindTime.title",
        "cover_key": "blog.posts.whereToFindTime.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/why-a-coach-needs-a-system/index.html",
        "uk": "/blog/why-a-coach-needs-a-system/",
        "title_key": "blog.posts.whyACoachNeedsASystem.metaTitle",
        "desc_key": "blog.posts.whyACoachNeedsASystem.description",
        "headline_key": "blog.posts.whyACoachNeedsASystem.title",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/free-consultations-and-workouts-ok-or-not/index.html",
        "uk": "/blog/free-consultations-and-workouts-ok-or-not/",
        "title_key": "blog.posts.freeConsultsAndWorkouts.metaTitle",
        "desc_key": "blog.posts.freeConsultsAndWorkouts.description",
        "headline_key": "blog.posts.freeConsultsAndWorkouts.title",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/should-a-coach-grow-social-media/index.html",
        "uk": "/blog/should-a-coach-grow-social-media/",
        "title_key": "blog.posts.shouldACoachGrowSocialMedia.metaTitle",
        "desc_key": "blog.posts.shouldACoachGrowSocialMedia.description",
        "headline_key": "blog.posts.shouldACoachGrowSocialMedia.title",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/why-potential-clients-dont-stay/index.html",
        "uk": "/blog/why-potential-clients-dont-stay/",
        "title_key": "blog.posts.whyPotentialClientsDontStay.metaTitle",
        "desc_key": "blog.posts.whyPotentialClientsDontStay.description",
        "headline_key": "blog.posts.whyPotentialClientsDontStay.title",
        "cover_key": "blog.posts.whyPotentialClientsDontStay.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/is-coaching-not-for-you/index.html",
        "uk": "/blog/is-coaching-not-for-you/",
        "title_key": "blog.posts.isCoachingNotForYou.metaTitle",
        "desc_key": "blog.posts.isCoachingNotForYou.description",
        "headline_key": "blog.posts.isCoachingNotForYou.title",
        "cover_key": "blog.posts.isCoachingNotForYou.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/secret-principle-of-finding-clients/index.html",
        "uk": "/blog/secret-principle-of-finding-clients/",
        "title_key": "blog.posts.secretPrincipleOfFindingClients.metaTitle",
        "desc_key": "blog.posts.secretPrincipleOfFindingClients.description",
        "headline_key": "blog.posts.secretPrincipleOfFindingClients.title",
        "cover_key": "blog.posts.secretPrincipleOfFindingClients.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/why-clients-quit-training-even-with-results/index.html",
        "uk": "/blog/why-clients-quit-training-even-with-results/",
        "title_key": "blog.posts.whyClientsQuitEvenWithResults.metaTitle",
        "desc_key": "blog.posts.whyClientsQuitEvenWithResults.description",
        "headline_key": "blog.posts.whyClientsQuitEvenWithResults.title",
        "cover_key": "blog.posts.whyClientsQuitEvenWithResults.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/five-sales-techniques-for-coaches/index.html",
        "uk": "/blog/five-sales-techniques-for-coaches/",
        "title_key": "blog.posts.fiveSalesTechniquesForCoaches.metaTitle",
        "desc_key": "blog.posts.fiveSalesTechniquesForCoaches.description",
        "headline_key": "blog.posts.fiveSalesTechniquesForCoaches.title",
        "cover_key": "blog.posts.fiveSalesTechniquesForCoaches.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/excel-and-telegram-are-not-a-crm-for-coaches/index.html",
        "uk": "/blog/excel-and-telegram-are-not-a-crm-for-coaches/",
        "title_key": "blog.posts.excelAndTelegramAreNotACrm.metaTitle",
        "desc_key": "blog.posts.excelAndTelegramAreNotACrm.description",
        "headline_key": "blog.posts.excelAndTelegramAreNotACrm.title",
        "cover_key": "blog.posts.excelAndTelegramAreNotACrm.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/crm-for-personal-trainers/index.html",
        "uk": "/blog/crm-for-personal-trainers/",
        "title_key": "blog.posts.crmForPersonalTrainers.metaTitle",
        "desc_key": "blog.posts.crmForPersonalTrainers.description",
        "headline_key": "blog.posts.crmForPersonalTrainers.title",
        "cover_key": "blog.posts.crmForPersonalTrainers.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/official-launch/index.html",
        "uk": "/blog/official-launch/",
        "title_key": "blog.posts.officialLaunch.metaTitle",
        "desc_key": "blog.posts.officialLaunch.description",
        "headline_key": "blog.posts.officialLaunch.title",
        "cover_key": "blog.posts.officialLaunch.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/why-coaches-burn-out/index.html",
        "uk": "/blog/why-coaches-burn-out/",
        "title_key": "blog.posts.whyCoachesBurnOut.metaTitle",
        "desc_key": "blog.posts.whyCoachesBurnOut.description",
        "headline_key": "blog.posts.whyCoachesBurnOut.title",
        "cover_key": "blog.posts.whyCoachesBurnOut.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
    {
        "src": "blog/five-autumn-content-topics-for-coaches/index.html",
        "uk": "/blog/five-autumn-content-topics-for-coaches/",
        "title_key": "blog.posts.fiveAutumnContentTopics.metaTitle",
        "desc_key": "blog.posts.fiveAutumnContentTopics.description",
        "headline_key": "blog.posts.fiveAutumnContentTopics.title",
        "cover_key": "blog.posts.fiveAutumnContentTopics.cover",
        "changefreq": "monthly",
        "priority": "0.5",
    },
]

LOCALIZED_PATH = re.compile(
    r"^/(?:for-clients|support|privacy-policy|terms-and-conditions|coach|blog(?:/[\w-]+)?)?/?$"
)
PRELOAD_LANG = re.compile(
    r'var lang = path === "/en" \|\| path\.indexOf\("/en/"\) === 0 \? "en" : "ua";'
    r'|var lang = "ua";\s*'
    r'if \(path === "/en" \|\| path\.indexOf\("/en/"\) === 0\) lang = "en";\s*'
    r'else if \(path === "/pl" \|\| path\.indexOf\("/pl/"\) === 0\) lang = "pl";',
    re.S,
)
PRELOAD_REPLACEMENT = (
    'var lang = "ua";\n'
    '        if (path === "/en" || path.indexOf("/en/") === 0) lang = "en";\n'
    '        else if (path === "/pl" || path.indexOf("/pl/") === 0) lang = "pl";'
)
HREFLANG_CLUSTER = re.compile(
    r'(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+"\s*>\s*)+'
)
OG_LOCALE_CLUSTER = re.compile(
    r'<meta property="og:locale" content="[^"]*">'
    r'(?:\s*<meta property="og:locale:alternate" content="[^"]*">)*'
)
LANG_SWITCH = re.compile(
    r'(?:<div|<a)[^>]*data-lang="ua"[^>]*>\s*UA\s*</(?:div|a)>\s*'
    r'(?:<div|<a)[^>]*data-lang="en"[^>]*>\s*EN\s*</(?:div|a)>'
    r'(?:\s*(?:<div|<a)[^>]*data-lang="pl"[^>]*>\s*PL\s*</(?:div|a)>)?',
    re.S,
)


def get_nested(obj, key):
    cur = obj
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def find_close(html: str, after_open: int, tag: str):
    open_re = re.compile(rf"<{tag}\b", re.I)
    close_re = re.compile(rf"</{tag}\s*>", re.I)
    i = after_open
    depth = 1
    while i < len(html) and depth:
        open_m = open_re.search(html, i)
        close_m = close_re.search(html, i)
        if close_m is None:
            return None, None
        if open_m and open_m.start() < close_m.start():
            gt = html.find(">", open_m.start())
            if gt == -1:
                return None, None
            snippet = html[open_m.start() : gt + 1]
            i = gt + 1
            if snippet.rstrip().endswith("/>"):
                continue
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return close_m.start(), close_m.end()
            i = close_m.end()
    return None, None


def set_attr(attrs: str, name: str, value: str) -> str:
    pattern = re.compile(rf'\s{name}="[^"]*"', re.I)
    replacement = f' {name}="{html_lib.escape(value, quote=True)}"'
    if pattern.search(attrs):
        return pattern.sub(replacement, attrs, count=1)
    return attrs.rstrip() + replacement


def apply_attr_i18n(html: str, dictionary: dict, attr_name: str, html_attr: str) -> str:
    pattern = re.compile(rf"<[^>]*\s{attr_name}=\"([^\"]+)\"[^>]*>", re.S)

    def repl(match: re.Match) -> str:
        key = match.group(1)
        value = get_nested(dictionary, key)
        if not isinstance(value, str):
            return match.group(0)
        return set_attr_in_tag(match.group(0), html_attr, value)

    return pattern.sub(repl, html)


def set_attr_in_tag(tag: str, name: str, value: str) -> str:
    pattern = re.compile(rf'\s{name}="[^"]*"', re.I)
    replacement = f' {name}="{html_lib.escape(value, quote=True)}"'
    if pattern.search(tag):
        return pattern.sub(replacement, tag, count=1)
    if tag.endswith("/>"):
        return tag[:-2].rstrip() + replacement + " />"
    return tag[:-1] + replacement + ">"


def apply_text_i18n(html: str, dictionary: dict, attr: str, as_html: bool) -> str:
    pattern = re.compile(rf"<([a-zA-Z][\w:-]*)([^>]*\s{attr}=\"([^\"]+)\"[^>]*)>", re.S)
    out = []
    i = 0
    for match in pattern.finditer(html):
        key = match.group(3)
        value = get_nested(dictionary, key)
        out.append(html[i : match.start()])
        if not isinstance(value, str):
            out.append(match.group(0))
            i = match.end()
            continue
        tag = match.group(1)
        close_start, close_end = find_close(html, match.end(), tag)
        if close_start is None:
            out.append(match.group(0))
            i = match.end()
            continue
        if as_html:
            inner = value
        elif "\n" in value:
            inner = "<br>".join(html_lib.escape(part) for part in value.split("\n"))
        else:
            inner = html_lib.escape(value)
        out.append(match.group(0) + inner + html[close_start:close_end])
        i = close_end
    out.append(html[i:])
    return "".join(out)


def apply_i18n(html: str, dictionary: dict) -> str:
    html = apply_attr_i18n(html, dictionary, "data-i18n-content", "content")
    html = apply_attr_i18n(html, dictionary, "data-i18n-alt", "alt")
    html = apply_attr_i18n(html, dictionary, "data-i18n-src", "src")
    html = apply_attr_i18n(html, dictionary, "data-i18n-href", "href")
    html = apply_attr_i18n(html, dictionary, "data-i18n-aria", "aria-label")
    html = apply_text_i18n(html, dictionary, "data-i18n-html", True)
    html = apply_text_i18n(html, dictionary, "data-i18n", False)
    return html


def strip_locale_prefix(path: str) -> str:
    match = re.match(r"^/(en|pl)(/.*)?$", path)
    if match:
        return match.group(2) or "/"
    return path


def localized_path(uk_path: str, dict_lang: str) -> str:
    if dict_lang == "ua":
        return uk_path
    prefix = dict_lang
    if uk_path == "/":
        return f"/{prefix}/"
    return f"/{prefix}{uk_path}"


def dest_for(uk_path: str, dict_lang: str) -> str:
    loc = localized_path(uk_path, dict_lang)
    if loc.endswith("/"):
        return f"{loc[1:]}index.html"
    return f"{loc[1:]}/index.html"


def to_locale_url(url: str, dict_lang: str) -> str:
    hash_part = ""
    query = ""
    if "#" in url:
        url, hash_rest = url.split("#", 1)
        hash_part = "#" + hash_rest
    if "?" in url:
        url, query_rest = url.split("?", 1)
        query = "?" + query_rest
    origin = ""
    path = url
    if url.startswith(ORIGIN):
        origin = ORIGIN
        path = url[len(ORIGIN) :] or "/"
    path = strip_locale_prefix(path)
    if path in {"", "/"}:
        loc = localized_path("/", dict_lang)
        return f"{origin}{loc}{query}{hash_part}".replace("/?", "?")
    if LOCALIZED_PATH.match(path):
        if not path.endswith("/"):
            path += "/"
        loc = localized_path(path, dict_lang)
        return f"{origin}{loc}{query}{hash_part}"
    return (origin + path if origin else url) + query + hash_part


def rewrite_localized_hrefs(html: str, dict_lang: str) -> str:
    pattern = re.compile(
        r'(<a\b(?![^>]*\bdata-lang=)[^>]*?\shref=")([^"]+)(")',
        re.S | re.I,
    )

    def repl(match: re.Match) -> str:
        url = match.group(2)
        if url.startswith("#") or url.startswith("mailto:") or url.startswith("tel:"):
            return match.group(0)
        if url.startswith("http") and not url.startswith(ORIGIN):
            return match.group(0)
        return match.group(1) + to_locale_url(url, dict_lang) + match.group(3)

    return pattern.sub(repl, html)


def hreflang_block(page: dict) -> str:
    lines = []
    for dict_lang in ("ua", "en", "pl"):
        href = ORIGIN + localized_path(page["uk"], dict_lang)
        hreflang = LOCALES[dict_lang]["hreflang"]
        lines.append(f'<link rel="alternate" hreflang="{hreflang}" href="{href}">')
    default_href = ORIGIN + page["uk"]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{default_href}">')
    return "\n  ".join(lines) + "\n  "


def og_locale_block(dict_lang: str) -> str:
    primary = LOCALES[dict_lang]["og"]
    others = [LOCALES[code]["og"] for code in ("ua", "en", "pl") if code != dict_lang]
    lines = [f'<meta property="og:locale" content="{primary}">']
    lines.extend(
        f'<meta property="og:locale:alternate" content="{og}">' for og in others
    )
    return "\n  ".join(lines)


def rewrite_head_locale(html: str, page: dict, dict_lang: str) -> str:
    abs_url = ORIGIN + localized_path(page["uk"], dict_lang)
    html_lang = LOCALES[dict_lang]["html_lang"]
    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{html_lang}"', html, count=1)
    html = re.sub(
        r'<link rel="canonical" href="[^"]*"',
        f'<link rel="canonical" href="{abs_url}"',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:url" content="[^"]*"',
        f'<meta property="og:url" content="{abs_url}"',
        html,
        count=1,
    )
    html, og_count = OG_LOCALE_CLUSTER.subn(og_locale_block(dict_lang), html, count=1)
    if og_count == 0:
        raise SystemExit(f"No og:locale found in {page['src']}")
    html, href_count = HREFLANG_CLUSTER.subn(hreflang_block(page), html, count=1)
    if href_count == 0:
        raise SystemExit(f"No hreflang cluster found in {page['src']}")
    return html


def update_json_ld(html: str, page: dict, dict_lang: str, title: str, description: str, dictionary: dict) -> str:
    pattern = re.compile(
        r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        re.S,
    )
    abs_url = ORIGIN + localized_path(page["uk"], dict_lang)
    headline = get_nested(dictionary, page.get("headline_key") or "")
    if not isinstance(headline, str):
        headline = title
    cover = get_nested(dictionary, page.get("cover_key") or "")
    cover_abs = None
    if isinstance(cover, str):
        if cover.startswith("http"):
            cover_abs = cover
        elif cover.startswith("/"):
            cover_abs = ORIGIN + cover
    blog_title = get_nested(dictionary, "blog.title")

    def localize_origin_url(url: str) -> str:
        if not url.startswith(ORIGIN):
            return url
        path = strip_locale_prefix(url[len(ORIGIN):] or "/")
        if path not in {"", "/"} and not path.endswith("/"):
            path += "/"
        return ORIGIN + localized_path(path, dict_lang)

    def repl(match: re.Match) -> str:
        data = json.loads(match.group(1))
        webpage_id = abs_url + "#webpage"
        for node in data.get("@graph", []):
            node_type = node.get("@type")
            if node_type == "WebSite":
                node["inLanguage"] = ["uk-UA", "en-US", "pl-PL"]
            if node_type in {"WebPage", "CollectionPage"}:
                node["url"] = abs_url
                node["@id"] = webpage_id
                node["inLanguage"] = LOCALES[dict_lang]["schema"]
                node["name"] = title
                node["description"] = description
                if cover_abs and isinstance(node.get("primaryImageOfPage"), dict):
                    node["primaryImageOfPage"]["url"] = cover_abs
                if "breadcrumb" in node:
                    node["breadcrumb"] = {"@id": abs_url + "#breadcrumb"}
            if node_type == "BlogPosting":
                node["url"] = abs_url
                node["@id"] = abs_url + "#article"
                node["inLanguage"] = LOCALES[dict_lang]["schema"]
                node["headline"] = headline
                node["description"] = description
                node["mainEntityOfPage"] = {"@id": webpage_id}
                if cover_abs and isinstance(node.get("image"), dict):
                    node["image"]["url"] = cover_abs
            if node_type == "BreadcrumbList":
                node["@id"] = abs_url + "#breadcrumb"
                for item in node.get("itemListElement", []):
                    item_url = item.get("item")
                    if isinstance(item_url, str):
                        item["item"] = localize_origin_url(item_url)
                    if item.get("position") == 2 and isinstance(blog_title, str):
                        item["name"] = blog_title
                    if item.get("position") == 3:
                        item["name"] = headline
            if node_type == "SoftwareApplication":
                node["description"] = description
                features = get_nested(dictionary, "coach.schema.featureList")
                if isinstance(features, list):
                    node["featureList"] = features
            if node_type == "FAQPage":
                node["@id"] = abs_url + "#faq"
                node["url"] = abs_url + "#faq"
                node["inLanguage"] = LOCALES[dict_lang]["schema"]
                faq_items = []
                for key in FAQ_ITEM_KEYS:
                    q = get_nested(dictionary, f"coach.faq.items.{key}.q")
                    a = get_nested(dictionary, f"coach.faq.items.{key}.a")
                    if isinstance(q, str) and isinstance(a, str):
                        faq_items.append(
                            {
                                "@type": "Question",
                                "name": q,
                                "acceptedAnswer": {"@type": "Answer", "text": a},
                            }
                        )
                if faq_items:
                    node["mainEntity"] = faq_items
            if node_type == "ItemList":
                for item in node.get("itemListElement", []):
                    item_url = item.get("url")
                    if isinstance(item_url, str):
                        item["url"] = localize_origin_url(item_url)
                    for slug, title_key in BLOG_POST_TITLE_KEYS.items():
                        if slug in str(item.get("url", "")):
                            post_title = get_nested(dictionary, title_key)
                            if isinstance(post_title, str):
                                item["name"] = post_title
                            break
        dumped = json.dumps(data, ensure_ascii=False, indent=2)
        return f'<script type="application/ld+json">\n  {dumped}\n  </script>'

    return pattern.sub(repl, html, count=1)


def lang_switch_markup(page: dict, active: str) -> str:
    links = []
    for dict_lang, meta in LOCALES.items():
        href = localized_path(page["uk"], dict_lang)
        cls = "localisation-item is-active" if active == dict_lang else "localisation-item"
        links.append(
            f'<a class="{cls}" href="{href}" hreflang="{meta["hreflang"]}" '
            f'lang="{meta["html_lang"]}" data-lang="{dict_lang}" '
            f'data-i18n-aria="{meta["aria"]}">{meta["label"]}</a>'
        )
    return "\n            ".join(links)


def replace_lang_switchers(html: str, page: dict, active: str) -> str:
    markup = lang_switch_markup(page, active)
    updated, count = LANG_SWITCH.subn(markup, html)
    if count == 0:
        raise SystemExit(f"No language switchers found in {page['src']}")
    return updated


def patch_source_seo(html: str, page: dict) -> str:
    html, _ = PRELOAD_LANG.subn(PRELOAD_REPLACEMENT, html, count=1)
    html = html.replace("main.js?v=20260920", f"main.js?v={SCRIPT_VERSION}")
    html = html.replace("main.js?v=20260921", f"main.js?v={SCRIPT_VERSION}")
    html = html.replace("main.js?v=20260922", f"main.js?v={SCRIPT_VERSION}")
    html = html.replace("main.js?v=20260923", f"main.js?v={SCRIPT_VERSION}")
    html = html.replace(
        '"inLanguage": ["uk-UA", "en-US"]',
        '"inLanguage": ["uk-UA", "en-US", "pl-PL"]',
    )
    html = rewrite_head_locale(html, page, "ua")
    return html


def build_page(page: dict, dict_lang: str, dictionary: dict) -> None:
    src = ROOT / page["src"]
    html = src.read_text(encoding="utf-8")
    title = get_nested(dictionary, page["title_key"])
    desc = get_nested(dictionary, page["desc_key"])
    html = apply_i18n(html, dictionary)
    html = rewrite_localized_hrefs(html, dict_lang)
    html = rewrite_head_locale(html, page, dict_lang)
    html = update_json_ld(html, page, dict_lang, title, desc, dictionary)
    html = replace_lang_switchers(html, page, dict_lang)
    dest_rel = dest_for(page["uk"], dict_lang)
    dest = ROOT / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"wrote {dest_rel}")


def patch_source_pages() -> None:
    for page in PAGES:
        path = ROOT / page["src"]
        html = path.read_text(encoding="utf-8")
        html = patch_source_seo(html, page)
        html = replace_lang_switchers(html, page, "ua")
        path.write_text(html, encoding="utf-8")
        print(f"patched source {page['src']}")


def write_sitemap() -> None:
    blocks = []
    for page in PAGES:
        for dict_lang in ("ua", "en", "pl"):
            loc = ORIGIN + localized_path(page["uk"], dict_lang)
            links = []
            for alt_lang in ("ua", "en", "pl"):
                href = ORIGIN + localized_path(page["uk"], alt_lang)
                hreflang = LOCALES[alt_lang]["hreflang"]
                links.append(
                    f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="{href}"/>'
                )
            links.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN + page["uk"]}"/>'
            )
            blocks.append(
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                "    <lastmod>2026-09-21</lastmod>\n"
                f"    <changefreq>{page['changefreq']}</changefreq>\n"
                f"    <priority>{page['priority']}</priority>\n"
                + "\n".join(links)
                + "\n  </url>"
            )
    for extra in UA_ONLY_SITEMAP:
        loc = ORIGIN + extra["uk"]
        blocks.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            "    <lastmod>2026-09-21</lastmod>\n"
            f"    <changefreq>{extra['changefreq']}</changefreq>\n"
            f"    <priority>{extra['priority']}</priority>\n"
            f'    <xhtml:link rel="alternate" hreflang="uk" href="{loc}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>\n'
            "  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(blocks)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("wrote sitemap.xml")


def main() -> None:
    patch_source_pages()
    for dict_lang in GENERATED_LANGS:
        dictionary = json.loads(
            (ROOT / "locales" / f"{dict_lang}.json").read_text(encoding="utf-8")
        )
        for page in PAGES:
            build_page(page, dict_lang, dictionary)
    write_sitemap()


if __name__ == "__main__":
    main()
