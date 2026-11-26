# uniqaiapp.github.io

Hub site for the open-source tools from [UniqAI](https://uniqai.app/): https://uniqaiapp.github.io/

It links to the four live tools (each is served from its own repo at `/<repo>/`) and lists every repository in the [uniqaiapp](https://github.com/uniqaiapp) organisation. The root `robots.txt` here is the one crawlers read for all project sites, so it must never block anything and lists every tool sitemap.

| Path | Source repo |
|:---|:---|
| `/video-director/` | https://github.com/uniqaiapp/video-director |
| `/awesome-ai-video-prompts/` | https://github.com/uniqaiapp/awesome-ai-video-prompts |
| `/ugc-ad-director/` | https://github.com/uniqaiapp/ugc-ad-director |
| `/no-plastic/` | https://github.com/uniqaiapp/no-plastic |

## Build

Static files, standard library only. `index.html`, `sitemap.xml`, `robots.txt` and `llms.txt` are generated from `scripts/site.py`:

```bash
python3 scripts/site.py          # regenerate
python3 scripts/site.py --check  # fail if stale, JSON-LD invalid or a local link is missing
```

`assets/social-preview.png` (1280x640) is composed from the tools' own previews.

## Verification files

<!-- Place the Google Search Console verification file (google<hash>.html) and the Bing Webmaster verification file (BingSiteAuth.xml) in the repo root, next to the IndexNow key file. -->

The IndexNow key file is `<key>.txt` in the root; its content is the key.

Made by UniqAI. Curated by [Vlad Yasinski](https://www.roimobi.com). Code MIT.
