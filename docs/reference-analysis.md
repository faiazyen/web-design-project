# Reference analysis — Bachata Geneva Festival (bachatagenevafestival.com)

Analysed on 2026-10-19 with Firecrawl (page text, links, metadata). Used for **inspiration of structure and patterns only**. No text, images or code are copied. The reference is built with Next.js/React, which our rules forbid, so everything is rebuilt as plain HTML/CSS/JS.

**Not inspected:** visual design (fonts, spacing, animation), the interactive venue maps, the dropdown contents of the top navigation, `/terms`, `/privacy`, `/hq` (private team dashboard). Colour is known only from `theme-color: #ff9900`. A screenshot review in the browser is still needed for the visual layer.

## 1. Site map (observed)

| Page | URL | Purpose |
|---|---|---|
| Home | `/` | Hero with dates and price, look-back gallery, nations counter, pass box, venue, FAQ, partners |
| About | `/about` | Mission, vision, 8 numbered values, call to action |
| Team | `/team` | Member cards with role filter and name search |
| Venue & Maps | `/venue` | Four interactive level maps, links to travel pages |
| Getting around | `/getting-around` | Transport card, taxi, bikes, parking, shuttles |
| Accommodation | `/accommodation` | Partner hotels with filters, prices per night |
| Tickets | `/tickets` | Passes, price evolution by period |
| Programme | `/program` | Day-by-day schedule, opening and closing parties, city tours |
| Nations | `/nations` | Live count by continent and country, tag filters |
| Ambassadors | `/ambassadors` | Programme, benefits, application form, world map |
| Volunteers | `/volunteers` | Volunteer vs staff, departments, timeline, fine print, FAQ |
| Master Classes | `/masterclasses` | One class per day, price, rules |
| Round Table | `/roundtable` | Event page: concept, process, panel, FAQ |
| Global Bachata Summit | `/summit` | Event page: format, timed line-up, process, FAQ |
| Royal Rumble | `/royal-rumble` | Competition page: format, prize, registration |
| Press Corner | `/press-corner` | Press kit, media library, accreditation |
| Responsibility | `/responsibility` | Transport, energy, waste, food, people, local impact |
| We Care | `/we-care` | Code of conduct, how to report |
| Promote Your Event | `/promote` | Paid promotion packages with public prices |
| Terms, Privacy | `/terms`, `/privacy` | Legal |

Top navigation shows four groups: **Festival, Travel, About Us, Support**. The footer repeats about 16 links under "Navigate", plus contact email, social links and a community-chat link.

## 2. Patterns worth taking

1. **Hero with the three essentials above the fold:** dates, venue, price, one clear button. A second, quieter link follows ("Relive…").
2. **Repeated rhythm of sections:** small eyebrow label, large `h2`, one intro sentence, then content. Predictable and easy to scan.
3. **Numbered step lists** ("How it works") used on every participation page (volunteers, summit, round table). Strong for process content.
4. **Event pages share one template:** concept, process with dates, people, FAQ, closing call to action. This maps well to our workshop and artist templates.
5. **Filter + search on the team page:** role chips and a name field with a "Showing 3 of 3" counter. Good model for our Artists and Workshops lists.
6. **FAQ as an accordion** with numbered questions (home) and per-page FAQ blocks.
7. **Honest "fine print, upfront" sections** and a visible Code of Conduct. Builds trust and fits our accessibility and community tone.
8. **Look-back photo grid with captions** and photographer credit on every image. Supports our rule to record image sources.
9. **Counters and stats strip** (80+ nations, 32 artists). Good for the home page.
10. **Partner wall** grouped by tier (institutional, official, supporters).
11. **Price evolution table** on Tickets: shows when the price rises, creating a reason to buy early.
12. **Venue page with downloadable map** and "first fifteen minutes" links to Getting around, Accommodation, Passes.

## 3. Gaps in the reference that our spec fixes

- **No site search and no breadcrumbs** were found. Our spec requires both, so this is a place to be better, not to copy.
- **Navigation relies on hash links** (`/#tickets`, `/#faq`). Our spec uses real pages for Tickets and FAQ.
- **Pages are JavaScript-rendered**, so there is no guarantee they work without scripting. Ours are static HTML, with JS only for filter and search.
- **Metadata is inconsistent:** many pages reuse the home page's `og:title`, and 2026 and 2027 data are mixed (for example the Tickets page lists €199 while the home page shows €140 for 2027). Our rules require a specific title, description and canonical on every page, with JSON-LD matching the visible text.
- **Heavy partner and sponsor content** that a fictional festival does not need in full.

## 4. Proposed adaptations for Raíces del Mar (not yet in the spec)

The spec is binding, so these are proposals to approve before they enter `project-specification.md`.

| Idea from the reference | Adapted for us | Spec impact |
|---|---|---|
| Nations page | **"Roots" page**: the story of bachata dominicana with a short timeline | Could merge into *The Festival* page, no new page |
| Round Table / Summit event pages | **Talks & Live Music** items inside Programme, with detail template | Reuses workshop template |
| Volunteers page | **Volunteers** page (optional) | Would add 1 page, about 8% of the sitemap |
| We Care / Code of Conduct | **Code of Conduct** section on FAQ or a short page | Small addition |
| Responsibility | Sea-themed **Sustainability** note (beach, waste) | Section inside Venue & Travel |
| Hotels with filters | Accommodation list inside **Venue & Travel** with filter by distance and price | Reuses filter script |
| Price evolution | Price-by-period table on **Tickets** | Data only |
| Partner wall | Small **Partners** row in the footer or on Home | Data only |

## 5. Design notes to carry into the visual direction

- Warm, high-energy accent colour on a mostly dark or photographic background. For us, a sunset palette (coral, amber, deep sea blue) must still reach 4.5:1 contrast for text.
- Large photography with captions and credits. We must use AI-generated or free-licensed images and record each source.
- Generous spacing, one idea per section, short sentences.

## 6. Sources checked

Pages fetched: `/`, `/about`, `/team`, `/venue`, `/nations`, `/ambassadors`, `/volunteers`, `/roundtable`, `/summit`, `/royal-rumble`, `/masterclasses`, `/press-corner`, `/responsibility`, `/we-care`, `/promote`, `/tickets`, `/program`, `/getting-around`, `/accommodation`. Several were read as summaries, so wording, not structure, may differ from the live page.

## 7. Visual and navigation findings (added after browser inspection, 2026-10-19)

Observed in the browser and from Firecrawl branding data. Treat colour and font values as approximate (extractor confidence about 70%).

- **Mood:** dark, high-energy, nightclub. Near-black background (`rgb(10,0,0)`), warm amber accent (`#FFB347`, theme colour `#ff9900`), cream links (`#D3BDA8`).
- **Type:** League Spartan for headings (hero h1 about 128px), Montserrat for body text. Big, confident headline, wide letter-spaced small caps for labels (dates, venue, "Full Pass").
- **Shapes:** fully rounded pill buttons, 3px base radius on cards.
- **Hero:** full-bleed party photo with a dark overlay, an eyebrow chip ("Thank you, BGF26 · See you in 2027"), a Spanish headline (*¿Repetimos?*), one line of copy, a dates-and-venue row, then a price card with one primary button.
- **Navigation:** logo plus four dropdown groups (**Festival, Travel, About Us, Support**) and one icon button. Desktop only was checked; the mobile menu was not.
- **Cookie banner:** appears on first load with *Customize*, *Reject All* and *Accept All*. Rejecting is one click, which we should copy as a principle if we ever need a banner. Our site stores only the visitor's own schedule locally, so a short plain-language storage notice is enough.
- **Confirmed gaps:** there is **no search field and no breadcrumb** anywhere (checked in the live DOM). Both are required for us.
- **Stack:** Next.js with Tailwind. Not allowed for us.

## 8. What our festival is missing: ideas for the "Latino Mar" vibe

Ideas only. Each one that enters the spec needs approval, because the spec is binding.

| # | Idea | Why it adds to the vibe | Fits our rules? |
|---|---|---|---|
| 1 | **Day / Night mode** for the whole site: sand-and-turquoise by day, deep navy and amber by night, plus a toggle and respect for the system setting | Makes "sea by day, club by night" visible on every page, not just in the text | Yes, CSS variables and a few lines of JS. Both themes must reach AA contrast. |
| 2 | **Day / Night badge and filter** on every programme item | Beginners find beach workshops, night owls find club socials | Yes, uses the existing filter |
| 3 | **Spanish-flavoured microcopy** (headline, button labels, section eyebrows) with English meaning always present | Gives personality like the reference's *¿Repetimos?* without hurting accessibility | Yes. Add `lang="es"` on Spanish phrases. |
| 4 | **"Primera Ola" (first wave)** as the name of the 1st edition | A built-in story for a new festival | Content only |
| 5 | **Sunset Social** as a daily signature event at the beach stage | A recognisable ritual the site can repeat on Home, Programme and Venue | Data only |
| 6 | **Interactive SVG venue map** with clickable zones (beach stage, pavilion, club, workshop hall) | Matches the reference's strongest feature, built with plain SVG and JS | Yes, works from `file://` |
| 7 | **"Which level am I?"** mini-quiz for beginners | Serves the beginner-friendly goal and the first-timer scenario | Yes, plain JS |
| 8 | **Level and role tags with icons**, never colour alone (beginner, intermediate, advanced, lead, follow) | Clear, and accessible | Yes |
| 9 | **Roots timeline** on the Roots page: origins of bachata dominicana, instruments (guitar, requinto, güira), and its UNESCO listing (*date and wording to be verified before use*) | Our unique angle. Gives real cultural depth, not generic party copy | Content, simple list or CSS timeline |
| 10 | **Countdown** to opening night on Home | Energy and urgency | Yes, plain JS |
| 11 | **Stats strip** (days, venues, artists, sessions, countries) generated from `data.json` | Keeps numbers always correct | Yes, uses `data.js` |
| 12 | **My Programme with clash warnings and a downloadable calendar file** | Strong, useful interactive function | Yes. `localStorage` and a generated file download both work from `file://`. |
| 13 | **"What to pack and wear"** card (dance shoes on sand, sun, night dress code) | Practical, adds character | Content |
| 14 | **Image credit on every photo** | Required by our rules and mirrors the reference's credit lines | Yes |

**Identity guardrails so we do not copy the reference:** different palette (light-first with a night mode, turquoise, coral and sand rather than black and amber), different fonts (free-licensed and bundled locally, so the site works offline), different structure (Programme, Performers, Venues and My Programme as first-class pages), and original copy throughout.
