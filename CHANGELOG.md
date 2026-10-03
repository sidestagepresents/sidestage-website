# Changelog

## [1.0.0] — 2026-10-03

First production release. Live at https://sidestagepresents.com (apex; `www` pending).

### Stack

- **Eleventy** static site generator — builds in ~20s, zero runtime
- **Decap CMS** at `/admin/` — GitHub OAuth login, edit events/artists/pages/settings in the browser
- **GitHub** — content + code; every save auto-deploys
- **Cloudflare Pages** — hosting + CDN + DNS
- Total running cost: **$0/mo**

### What's in it

- **142 events** — 98 recovered from the Wayback Machine (old Squarespace site died), 35 backfilled from the Squarespace export, Instagram, and email, plus new 2026 shows
- **Upcoming** (soonest-first) and **Archive** (newest-first, grouped by year); past shows roll over automatically by date (Toronto time)
- **Artists** section with full bio pages for roster artists (Night Lovell first)
- **About / Privacy** pages
- **Minimal black design** — original logo used byte-for-byte, no filters; Neue Montreal headings (self-hosted woff2)
- **Mobile hamburger menu** (no JavaScript), responsive throughout
- **Menu control panel** (Site Settings → Menu): toggle pages, Instagram button, and a CTA button on/off
- **Drafts + scheduled publishing**: `draft` toggle hides anything instantly; `publish_at` embargo keeps a show hidden until announce time
- **SOLD OUT badge** replaces the Tickets button (same size)
- **Automatic image optimization**: upload any flyer, the build serves responsive WebP (400/800w) with JPEG fallback — no pre-compressing
- **UTM tags** (`utm_source=sidestagepresents.com`, `utm_medium=referral`) auto-appended to every outbound ticket link
- **SEO/sharing**: OpenGraph + Twitter cards (event flyers as share images), `robots.txt`, `sitemap.xml`, `llms.txt` generated from live listings
- **Favicon**, **Toronto-time date handling** (tonight's show doesn't vanish at 8pm ET)

### Performance

Static HTML + CDN: 97+ across the board on speed analytics. Nothing to tune — it's fast because there's almost nothing to load.

### Known follow-ups (post-1.0)

- `www` subdomain returns 522 until added under Pages → Custom domains
- Newsletter signup (Cloudflare Worker + KV) — spec'd, not built
- Scheduled auto-publish GitHub Action — written, needs adding via github.com (deploy token lacks `workflow` scope)
- Cloudflare Web Analytics toggle (Workers & Pages → Metrics → Enable)
- Roster list to settle with Andrew Pupolin
