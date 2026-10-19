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
