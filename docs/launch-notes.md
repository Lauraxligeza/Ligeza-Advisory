# Service architecture launch notes

The site uses static HTML, shared CSS and vanilla JavaScript. No hosting redirect configuration was found. The legacy pricing pages have been removed.

## Recommended permanent redirects

Configure HTTP 301 redirects on the production host. Match both directory URLs and their explicit `index.html` variants where applicable. Preserve query strings where appropriate.

| Old path | Destination |
| --- | --- |
| `/pricing/` | `/services/` |
| `/pricing/market-snapshot.html` | `/services/` |
| `/pricing/international-growth-partner/` | `/services/` |
| `/pricing/market-snapshot/` | `/services/` |
| `/pricing/market-launch-system/` | `/services/` |
| `/pricing/market-fit-check/` | `/services/` |
| `/pricing/page-level-review/` | `/services/` |
| `/pricing/multi-market-alignment/` | `/services/` |
| `/pricing/conversion-trust-sprint/` | `/services/` |
| `/pricing/seo-intent-check/` | `/services/` |

The research approach remains at `/markets/` to preserve existing links. The pricing overview has also been removed. Only current pages are in the sitemap.

## Production checks

- Verify HTTPS, domain redirects and delivery to contact@ligezaadvisory.com.
- The public contact form is inactive. Complete the privacy information and verify Formspree settings before restoring it.
- Clarity has been removed. Fonts are hosted locally. Check production hosting for injected tracking and server-side logging.
- The published Privacy Policy still contains owner-supplied completion fields; verify these before treating it as final.
- Old pricing URLs now require host-level redirects to `/services/` if existing external links should remain usable.

## Local checks

Run `python3 checks/site.py` and `python3 checks/privacy.py` after changes.
