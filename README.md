# neto-support

Privacy policy and support pages for the skills-il iOS apps, published with GitHub Pages
(Jekyll, `jekyll-theme-minimal`). Every page is bilingual Hebrew / English.

Live site: https://bluzername.github.io/neto-support/

## Pages

These are the URLs entered in App Store Connect as the privacy policy and support URLs.

| App | Page | Source | Public URL |
|-----|------|--------|------------|
| Neto (נטו) | Privacy policy | `privacy-policy.md` | https://bluzername.github.io/neto-support/privacy-policy |
| Neto (נטו) | Support | `support.md` | https://bluzername.github.io/neto-support/support |
| Kabala (קבלה בשנייה) | Privacy policy | `kabala-privacy.md` | https://bluzername.github.io/neto-support/kabala-privacy |
| Kabala (קבלה בשנייה) | Support | `kabala-support.md` | https://bluzername.github.io/neto-support/kabala-support |
| Zakaut (זכאות) | Privacy policy | `zakaut-privacy.md` | https://bluzername.github.io/neto-support/zakaut-privacy |
| Zakaut (זכאות) | Support | `zakaut-support.md` | https://bluzername.github.io/neto-support/zakaut-support |

`index.md` is the landing page that links to all of the above.

## zakaut-rates.json

`zakaut-rates.json` is a versioned data file fetched by the Zakaut app from
https://bluzername.github.io/neto-support/zakaut-rates.json (served as-is by GitHub Pages, no Jekyll
processing). Schema:

| Key | Type | Meaning |
|-----|------|---------|
| `version` | positive integer | Bump on every change so the app can detect a new release |
| `published` | string, `YYYY-MM-DD` | Real calendar date, never in the future |
| `tables` | object | One entry per rate table; every value must itself be an object |

`tables` is currently empty (the app ships with built-in rates). CI runs
`python3 scripts/validate_rates.py zakaut-rates.json` on every change to the file; run it locally
before committing. The script is stdlib-only and prints one line per violation.

## Editing

1. Edit the Markdown file for the page (keep the Hebrew section first, English second, as today).
2. Update the `Last updated:` line on privacy pages when the wording changes.
3. Commit to `main`. GitHub Pages rebuilds the site within a few minutes.

Adding a new app means adding two pages (`<app>-privacy.md`, `<app>-support.md`) and linking them
from `index.md`. Page URLs are the file name without `.md`.

## Local preview

Requires Ruby 3.x and Bundler. The `Gemfile` pins the `github-pages` gem so the local build matches
what GitHub Pages runs.

```sh
bundle install
bundle exec jekyll serve
```

Then open the local URL Jekyll prints (port 4000, path `/neto-support/`).

Without Ruby, `python3 -m http.server` only serves the raw `.md` files and `zakaut-rates.json`;
it does not render the Markdown or the theme, so use it only to check the JSON.

## Checks

- `.github/workflows/link-check.yml`: on push, pull request and weekly, checks every http(s) link in
  the Markdown files with lychee and curls the seven public URLs above expecting HTTP 200.
- `.github/workflows/validate-rates.yml`: validates `zakaut-rates.json` on every change.
- Dependabot keeps the GitHub Actions and the `github-pages` gem current (weekly).

## Contact

bluzerasi@gmail.com
