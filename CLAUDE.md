# DueThisWeek — Web

Turn the school PDFs and emails piling up in a parent's inbox into one checklist for the
week — across every kid in the household.

The web platform repository of the DueThisWeek container. `../CLAUDE.md` governs product
behavior, domain vocabulary, user-facing copy, and releases. This file governs how the site
is built and served.

**This is not the app, and it is not a mirror of it.** It is the static site carrying the
public documents the App Store requires — privacy policy, terms, support — plus whatever
marketing page the product grows. It has no layer folders because it has no layers, it is
not measured against iOS, and it implements nothing from `../docs/domain.md` except the copy
it quotes.

**The legal text is authored in the container, not here.** `../docs/domain.md`, *Copy*, is
the source; this repository renders it. A policy edited here and not there is a policy the
app's own disclosures no longer match — which is the exact discrepancy an App Review
rejection is written about.

## The tree

```
due-this-week-web/
├── CLAUDE.md
├── render-legal.py   generates privacy.html and terms.html from ../docs/domain.md
├── style.css         one stylesheet, colours defined once at the top
├── index.html        what the product is, and what it costs
├── privacy.html      GENERATED — do not edit
├── terms.html        GENERATED — do not edit
└── support.html      how to get in touch, and the questions people ask
```

**This tree is the single source of truth for this repository's structure. When a folder is
added, removed, or renamed, update it in the same change.**

## Status

Four pages, written and serving locally. **Hosting is not turned on** — see below, and it is
the one thing standing between this and a store submission.

**Stack:** plain HTML and CSS, hand-written, **no build step**. No framework, no package
manifest, no `node_modules`. Four documents that change a few times a year do not earn a
toolchain, and a toolchain is a thing that breaks between the day it is set up and the day the
site is urgently needed.

`render-legal.py` is the one exception and it is not a build step — it is a copier. See
**Generated content**.

**`support.html` carries a placeholder.** The contact address reads `SUPPORT_EMAIL` and must
be a real one before submission: App Review fetches the support URL and a page with no way to
reach anybody is a rejection. It is left as a placeholder deliberately rather than guessed —
publishing somebody's address is the owner's decision, not an assumption.

## Serving it — read this before the first App Store submission

| What | Value |
|---|---|
| Production URL | `https://graboosky.github.io/due-this-week-web/` |
| Host | GitHub Pages |
| DNS / registrar | none — no custom domain |

**There is a blocker on that plan, and it is better dealt with now than during a
submission.** `graboosky/due-this-week-web` is a **private** repository and the account is on
the **free** plan. GitHub Pages cannot publish from a private repository on a free plan, so
the URL above returns nothing until one of these happens:

1. **Make this repository public.** It is a legal and marketing site — its entire content is
   meant to be read by strangers — so there is nothing here to protect. This is the default
   answer and it is one setting. It is the owner's call, not an automatic one, which is why
   the repository was created private.
2. **Serve it from Cloudflare Pages or Netlify instead.** Both publish from a private
   repository on their free tiers. Choose this if the repository should stay private for a
   reason this file does not know about.

Whichever wins, record it in the table above and delete this list.

**The URLs must return 200 before any store submission**, because review fetches them and a
404 costs a review cycle. `../docs/release.md` puts web first in the ship order for exactly
this reason — it is the cheapest platform to ship and the one most likely to be forgotten
until the submission form asks for a privacy-policy URL.

## Build & test

There is no build. The files are served as written.

Check before pushing anything that review will fetch:

```bash
python3 -m http.server 8000        # then open http://localhost:8000
```

- Every page returns 200 and renders with CSS disabled.
- Every internal link resolves. A broken link between `privacy.html` and `terms.html` is
  invisible until someone follows it, and one of those someones is a reviewer.
- The pages are readable on a phone. Most people who open a privacy policy do it from a
  link inside an app.

## Generated content

If any page here is generated from another platform's source — legal text, screenshots,
pricing, release notes — say so **on the page and here**, with the command that regenerates
it. A file silently overwritten by an export script is a file someone will edit by hand and
lose.

- **`privacy.html` and `terms.html` are generated** from `../docs/domain.md` by
  `./render-legal.py`. Each carries an HTML comment saying so. Edit the contract, run the
  script, commit both.

```bash
./render-legal.py            # after any change to the legal text
./render-legal.py --check    # fails when a page is out of date
```

  The legal text is authored in the container because the app's own disclosures quote it. A
  policy edited here and not there is the exact discrepancy an App Review rejection is written
  about — which is why editing these two files directly loses the edit at the next run.

## Conventions

- **Copy comes from `../docs/domain.md`.** Writing a second version of a sentence here is how
  the product starts saying two different things — and for a privacy policy, that is not a
  style problem.
- **One stylesheet, hand-written, with the colors defined once at the top** as custom
  properties. This repository has no `designSystem/` folder and does not need one, but the
  rule behind that folder still applies: a hex value written twice is a hex value that will
  disagree with itself.
- **No analytics, no trackers, no embedded fonts from a third party.** A privacy policy
  served from a page that phones home is the one joke a reviewer will not find funny, and
  the product's whole pitch is that the documents never leave the parent's phone.
- **No JavaScript unless a page genuinely cannot work without it.** Nothing here needs it.

<TODO: the page shell — where the header, footer, and shared styles live once there is more
than one page to share them between.>
