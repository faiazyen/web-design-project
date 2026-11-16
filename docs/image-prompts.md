# Image sources

All images on the site are AI-generated or freely licensed (course rule). Every image in `data.json` has `credit` and `source` fields.

## Images in the site (2026-11-17)
| Files | What | Tool | How made |
|---|---|---|---|
| `web/images/avatars/*.svg` (12) | Illustrated avatars: 4 kinds (instructor, DJ, musician, show team) in 3 colour variants, used for all 64 performers | Claude Code (AI) | Drawn as code by `scripts/make-images.py`. No photos, no real people. |
| `web/images/venues/*.svg` (3) | Illustrated scenes for Arena Stage, Pabellón Brisa and Marea Club | Claude Code (AI) | Same script |
| `web/images/logo.svg`, `social-card.svg` | Sun logo and the picture used when the site is shared | Claude Code (AI) | Same script |
| The hero scene (Day and Night) | Sunset scene drawn in the page itself | Claude Code (AI) | Written into the page by `scripts/build-site.py` |

Change to the data foundation: the `image` fields of the performers and venues in `data.json` now point to these files (before, they pointed to photo files that did not exist yet). Reason: the team chose illustrated avatars for performers without their own photo, and vector art is small and fast.

## Not yet made (optional, later)
AI photos (hero stills, venues, featured artists) may be added if time allows. Log each prompt, tool and date here when they exist.

## Fonts
Fraunces and Source Sans 3 (SIL Open Font License), see `web/fonts/LICENSE.txt`.
