#!/usr/bin/env python3
"""Generate index.html, sitemap.xml, llms.txt, robots.txt for the UniqAI hub. Stdlib only.
  python3 scripts/site.py          write files
  python3 scripts/site.py --check  fail if files are stale, JSON-LD does not parse or a local link is missing
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://uniqaiapp.github.io/"
DATE = "2026-11-26"
UTM = "utm_source=github&utm_medium=pages&utm_campaign=hub"
PH_KEY = "phc_AVmhcac2jVRwi9asHEuhzJXnAbQA2hzfUxzWvzjyLPc8"
AUTHOR = {"@type": "Person", "name": "Vlad Yasinski", "url": "https://www.roimobi.com/",
          "sameAs": ["https://www.roimobi.com", "https://www.linkedin.com/in/vlad-yasinski-ua5er/", "https://github.com/ua5er"]}
TITLE = "Free AI Video and Image Prompt Tools, Open Source | UniqAI"
DESC = ("Free, open-source AI video and image prompt tools from UniqAI: a prompt gallery, a storyboard builder, "
        "a UGC ad script checker and an image prompt checker. They run in your browser.")

TOOLS = [
    {"slug": "video-director", "name": "Video Director", "kind": "Storyboard builder",
     "job": "Turn a one-line idea into a timed storyboard and a paste-ready AI video prompt.",
     "get": "A beat-by-beat shot list and one prompt per model, shaped for Kling 3.0, Veo 3, Wan 2.5, Seedance or Runway, with each model's length and audio limits applied.",
     "uniq": ("https://uniqai.app/video/text-to-video", "Make a video in UniqAI")},
    {"slug": "awesome-ai-video-prompts", "name": "AI Video Prompt Gallery", "kind": "Prompt gallery",
     "job": "Search real AI video prompts, filter by model and copy the one you need.",
     "get": "Each prompt comes with its model, mode, duration, aspect ratio and a short note on why the structure works. Free to reuse under CC BY 4.0.",
     "uniq": ("https://uniqai.app/video", "Open UniqAI video")},
    {"slug": "ugc-ad-director", "name": "UGC Ad Director", "kind": "Ad script checker",
     "job": "Check a UGC ad script before you spend money generating it.",
     "get": "A lint for the hook, the AI label, claims and fake testimonials, then a first-frame image prompt plus Kling and Veo 3 prompts for every shot.",
     "uniq": ("https://uniqai.app/video/image-to-video", "Animate an image in UniqAI")},
    {"slug": "no-plastic", "name": "no-plastic", "kind": "Image prompt checker",
     "job": "Stop AI portraits from looking plastic by fixing the prompt first.",
     "get": "A 0 to 100 score, the exact words that cause waxy skin and a fill-in photo brief to copy. It checks wording only and cannot see your image.",
     "uniq": ("https://uniqai.app/image/text-to-image", "Make an image in UniqAI")},
]
for t in TOOLS:
    t["url"] = f"{BASE}{t['slug']}/"
    t["repo"] = f"https://github.com/uniqaiapp/{t['slug']}"
    t["thumb"] = f"assets/thumb-{t['slug']}.jpg"

REPOS = [
    ("video-director", "Shot-by-shot AI video prompts in each model's own syntax."),
    ("awesome-ai-video-prompts", "Curated prompt list with model, mode, duration and aspect. CC BY 4.0."),
    ("ugc-ad-director", "UGC ad scripts with a lint that refuses fake reviews and unlabelled AI presenters."),
    ("ai-video-pricing", "AI video cost per second, with source URL and check date on every row."),
    ("no-plastic", "Rewrites an image prompt into a photographic brief and lints it."),
    ("suno-producer", "Suno style prompts, meta-tags and lyric structure, in English and Russian."),
    ("model-router", "Picks the cheapest LLM that still passes the task, with dated prices."),
    ("token-diet", "Rewrites a prompt into compact English and counts tokens before and after."),
    ("skill-shrinker", "Compresses SKILL.md and AGENTS.md files and checks every MUST and NEVER survived."),
    ("deslop-ru", "Finds and rewrites the phrases that make a Russian draft sound generated."),
]


def esc(s):
    return html.escape(s, quote=True)


def uq(url, content):
    return f"{url}?{UTM.replace('&', '&amp;')}&amp;utm_content={content}"


def jsonld():
    items = []
    for i, t in enumerate(TOOLS, 1):
        items.append({"@type": "ListItem", "position": i, "item": {
            "@type": "SoftwareApplication", "name": t["name"], "url": t["url"],
            "applicationCategory": "MultimediaApplication", "operatingSystem": "Any (web browser)",
            "description": t["job"], "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "image": f"{BASE}{t['thumb']}", "codeRepository": t["repo"]}})
    g = [
        {"@type": "Organization", "@id": "https://uniqai.app/#org", "name": "UniqAI", "url": "https://uniqai.app/",
         "logo": {"@type": "ImageObject", "url": "https://uniqai.app/icon-512.png", "width": 512, "height": 512},
         "sameAs": ["https://github.com/uniqaiapp"]},
        {"@type": "WebSite", "@id": BASE + "#site", "name": "UniqAI open-source tools", "url": BASE,
         "publisher": {"@id": "https://uniqai.app/#org"}, "inLanguage": "en"},
        {"@type": "CollectionPage", "@id": BASE + "#page", "url": BASE, "name": TITLE, "description": DESC,
         "inLanguage": "en", "dateModified": DATE, "isPartOf": {"@id": BASE + "#site"},
         "publisher": {"@id": "https://uniqai.app/#org"}, "author": {"@id": "https://www.roimobi.com/#vlad"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": BASE + "assets/social-preview.png"},
         "mainEntity": {"@type": "ItemList", "itemListElement": items}},
        dict(AUTHOR, **{"@id": "https://www.roimobi.com/#vlad"}),
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False, separators=(",", ":"))


def tool_html(i, t):
    u = t["uniq"]
    return f'''<article class="tool">
<a class="tool-img" href="{t['url']}" tabindex="-1" aria-hidden="true"><img src="{t['thumb']}" alt="" width="800" height="400" loading="lazy" decoding="async"></a>
<div><p class="tool-no">{i:02d} / {esc(t['kind'])}</p>
<h3><a href="{t['url']}">{esc(t['name'])}</a></h3>
<p class="job">{esc(t['job'])}</p>
<p class="get"><b>What you get.</b> {esc(t['get'])}</p>
<div class="tool-cta"><a class="btn" href="{t['url']}" data-out="tool-{t['slug']}">Try it in your browser</a><a class="btn btn-ghost" href="{t['repo']}" rel="noopener" data-out="repo-{t['slug']}">GitHub repo</a><a class="btn btn-ghost" href="{uq(u[0], 'tool-' + t['slug'])}" rel="noopener" data-out="uniqai-{t['slug']}">{esc(u[1])}</a></div></div>
</article>'''


def index_html():
    tools = "\n".join(tool_html(i, t) for i, t in enumerate(TOOLS, 1))
    repos = "".join(f'<li><a href="https://github.com/uniqaiapp/{s}" rel="noopener"><strong>{s}</strong><span>{esc(d)}</span></a></li>' for s, d in REPOS)
    og = BASE + "assets/social-preview.png"
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(TITLE)}</title>
<meta name="description" content="{esc(DESC)}">
<link rel="canonical" href="{BASE}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="UniqAI open source">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(TITLE)}">
<meta property="og:description" content="{esc(DESC)}">
<meta property="og:url" content="{BASE}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="640">
<meta property="og:image:alt" content="UniqAI open source: four free AI video and image prompt tools that run in your browser">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(TITLE)}">
<meta name="twitter:description" content="{esc(DESC)}">
<meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#0b1113">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/Geist-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="site.css">
<link rel="alternate" type="text/plain" href="{BASE}llms.txt" title="llms.txt">
<script type="application/ld+json">{jsonld()}</script>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<header class="top"><div class="wrap top-in">
<a class="brand" href="./" aria-label="UniqAI open-source tools"><img src="assets/wordmark.svg" alt="UniqAI" width="96" height="28"><span>open source</span></a>
<nav class="nav" aria-label="Sections"><a href="#tools">Tools</a><a href="#repos" class="hide-sm">Repositories</a><a href="https://github.com/uniqaiapp" rel="noopener" class="hide-sm">GitHub</a></nav>
<a class="btn btn-sm" href="{uq('https://uniqai.app/', 'header')}" data-out="header">Open UniqAI</a>
</div></header>
<main id="main">
<section class="hero"><div class="wrap hero-in">
<p class="pill"><span class="dot"></span>Free · MIT and CC BY 4.0 · no sign-up</p>
<h1>Free AI video and image prompt tools, <em>open source</em></h1>
<p class="lead"><a href="{uq('https://uniqai.app/', 'intro')}" rel="noopener" data-out="intro">UniqAI</a> is an app for AI photos, video and chat. These are the free tools we built around it: they write, check and collect the prompts that AI video and image models respond to. Each one runs in your browser, and the code is on GitHub.</p>
<div class="hero-cta"><a class="btn" href="#tools">Try in your browser</a><a class="btn btn-ghost" href="https://github.com/uniqaiapp" rel="noopener">All repositories</a></div>
</div></section>
<section class="tools wrap" id="tools" aria-labelledby="tools-h"><h2 id="tools-h">Try in your browser</h2>
<p class="sub">Four tools, nothing to install. Open one, paste or pick an idea, copy the result into the model you use.</p>
{tools}
</section>
<section class="repos wrap" id="repos" aria-labelledby="repos-h"><h2 id="repos-h">All repositories</h2>
<p class="sub">Every repo is one focused thing and uses only the Python or Node standard library.</p>
<ul class="repo-list">{repos}</ul></section>
<section class="also wrap" aria-labelledby="also-h"><h2 id="also-h">Sister project</h2>
<p>Music instead of video? <a href="https://hablamusic.github.io/suno-latin-producer/" rel="noopener">HablaMusic</a> builds free Suno prompts and lyrics for reggaeton, cumbia and funk carioca, and has its own <a href="https://github.com/hablamusic" rel="noopener">GitHub organisation</a>.</p>
<p>A note on models: UniqAI runs Nano Banana for images and Kling and Veo for video. Where a tool also writes prompts for other models, those notes are written for those models, which UniqAI does not run. Model names are trademarks of their owners.</p></section>
<section class="author wrap" aria-label="About the author"><p>Curated by <strong>Vlad Yasinski</strong>, AI growth consultant (<a href="https://www.roimobi.com/?{UTM.replace('&', '&amp;')}" rel="noopener">roimobi.com</a>, <a href="https://www.linkedin.com/in/vlad-yasinski-ua5er/" rel="noopener">LinkedIn</a>, <a href="https://github.com/ua5er" rel="noopener">GitHub</a>). Published with UniqAI. Only anonymous page views and button clicks are counted.</p></section>
</main>
<footer class="foot"><div class="wrap foot-in">
<p><strong>UniqAI</strong> makes AI photo, video and chat tools at <a href="{uq('https://uniqai.app/', 'footer')}" data-out="footer">uniqai.app</a>. The code on this site's tools is open source on <a href="https://github.com/uniqaiapp" rel="noopener">GitHub</a>.</p>
<p>Curated by <a href="https://www.roimobi.com/" rel="noopener">Vlad Yasinski</a> · <a href="https://www.linkedin.com/in/vlad-yasinski-ua5er/" rel="noopener">LinkedIn</a> · <a href="https://t.me/ua5er" rel="noopener">Telegram</a></p>
</div></footer>
<script>window.UQ={{key:"{PH_KEY}",repo:"hub"}};</script>
<script src="site.js" defer></script>
</body></html>
'''


def sitemap():
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>{BASE}</loc><lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>1.0</priority></url>
</urlset>
'''


def robots():
    lines = ["User-agent: *", "Allow: /", "", f"Sitemap: {BASE}sitemap.xml"]
    lines += [f"Sitemap: {t['url']}sitemap.xml" for t in TOOLS]
    return "\n".join(lines) + "\n"


def llms():
    out = ["# UniqAI open-source tools: free AI video and image prompt tools", "",
           "> Four free tools from UniqAI (https://uniqai.app/), an AI photo, video and chat app. They write, check and collect prompts for AI video and image models, run in the browser and are open source. Curated by Vlad Yasinski (https://www.linkedin.com/in/vlad-yasinski-ua5er/).", "",
           "## Tools", ""]
    out += [f"- [{t['name']}]({t['url']}): {t['kind']}. {t['job']} Repo: {t['repo']}" for t in TOOLS]
    out += ["", "## Other repositories", "", "- [uniqaiapp on GitHub](https://github.com/uniqaiapp): " + ", ".join(s for s, _ in REPOS),
            "- [HablaMusic suno-latin-producer](https://hablamusic.github.io/suno-latin-producer/): sister project, Suno prompts and lyrics for Latin genres", "",
            "## Facts", "",
            "- UniqAI runs Nano Banana for images and Kling and Veo for video.",
            "- Tool notes for other models (Wan, Seedance, Runway, Flux, Midjourney, SDXL and others) are written for those models, which UniqAI does not run.",
            "- Code is MIT licensed; prompt collections and vocabularies are CC BY 4.0.",
            "- The tools run in the browser. Only anonymous page views and button clicks are counted, never the text you type.", "",
            "## Author", "", "- Vlad Yasinski: https://www.roimobi.com, https://www.linkedin.com/in/vlad-yasinski-ua5er/, https://github.com/ua5er", ""]
    return "\n".join(out)


FILES = {"index.html": index_html, "sitemap.xml": sitemap, "robots.txt": robots, "llms.txt": llms}


def main():
    check = "--check" in sys.argv
    bad = 0
    for name, fn in FILES.items():
        want, p = fn(), ROOT / name
        if check:
            if not p.exists() or p.read_text() != want:
                print("STALE", name); bad += 1
        else:
            p.write_text(want); print("wrote", name)
    if check:
        src = (ROOT / "index.html").read_text()
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
            json.loads(m)
        for ref in re.findall(r'(?:src|href)="((?!https?:|#|mailto:)[^"]+)"', src):
            if not (ROOT / ref.split("?")[0]).exists() and ref != "./":
                print("MISSING", ref); bad += 1
        for f in ("assets/social-preview.png", "404.html", ".nojekyll"):
            if not (ROOT / f).exists():
                print("MISSING", f); bad += 1
        print("ok" if not bad else f"{bad} problem(s)")
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
