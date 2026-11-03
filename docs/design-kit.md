# Design kit: palette, type and image brief (for the real build)

**Status:** proposal, 2026-11-03. The Seminar 3 prototype stays **mid-fidelity grayscale** (team rule), so none of this is applied there. This kit is for the implementation phase.
**Brand idea:** *Atardecer* means sunset. The site has two moods: **Day (Sea)** and **Night (Club)**. Colour, type and images all serve those two moods.

## 1. Palette options

Every pair below was computed against WCAG contrast. Text needs 4.5:1 or more.

### Option A: Golden Hour (recommended)
Sunset coral and sea turquoise on warm cream by day, deep navy by night.

| Token | Day | Night |
|---|---|---|
| Background | `#FFF7EC` | `#0D1B2A` |
| Surface (cards) | `#FFFFFF` | `#14283C` |
| Text | `#1B2A41` | `#FDF3E7` |
| Muted text | `#4B5563` | `#B8C4D0` |
| Primary (buttons, key links) | `#C93A22` | `#FF7B5C` |
| Button text | `#FFFFFF` | `#0D1B2A` |
| Secondary (sea) | `#0B6E77` | `#57C7CE` |
| Highlight (badges, never body text) | `#F2A33A` | `#F5B04C` |

Contrast: text on background 13.6 (Day) and 15.9 (Night); muted text 7.1 and 9.8; button text on primary 5.1 and 6.8; secondary on background 5.6 and 8.7.

### Option B: Sea Glass
Cool and calm: deep teal with a soft coral accent.
Day: background `#F3FAFA`, text `#0F2D33`, primary `#0A6C74`, accent `#FF8A65`. Night: background `#071E22`, text `#EAF7F7`, primary `#4FD1C5`, accent `#FF9E80`.
Contrast: text 13.8 and 15.7; button text on primary 6.2 and 9.3.

### Option C: Raíz (roots)
Earthy and warm: terracotta, palm green and mango. Leans on the Dominican roots theme.
Day: background `#FBF3E4`, text `#2E2118`, primary `#B03F1C`, secondary `#2F6B3F`, accent `#E9A93B`. Night: background `#1D140E`, text `#F6E9D6`, primary `#F08A5D`, secondary `#7CC48A`.
Contrast: text 14.1 and 15.1; button text on primary 5.9 and 7.0.

**My recommendation: A.** The name is the sunset, so coral and gold carry the idea. Turquoise gives the sea. It reads as a warm light site by day and a distinct dark site by night. Option B is calmer but less festive. Option C is the most "roots" but the least "sea".

Rules for all options: never rely on colour alone (level and role tags use text and icons), and the highlight colour is only for badges with dark text on top, never for body text.

## 2. Typography (free, bundled locally)

The site must work from `file://` with no network, so fonts are downloaded once and shipped in `web/fonts/` (no CDN). Both options below are free under the SIL Open Font License.

| Option | Headings | Body | Mood |
|---|---|---|---|
| 1 (recommended) | Fraunces (soft serif) | Source Sans 3 | Warm, editorial, a little romantic |
| 2 | DM Serif Display | Inter | Clean, modern, more neutral |

Scale (mobile first): body 18 px, small 14 px, h3 22 px, h2 28 px, h1 36 px. Desktop h1 56 px. Line height 1.5 for body.

## 3. UI basics for the build
- Spacing scale on a 4 px base: 4, 8, 12, 16, 24, 32, 48.
- Radius: 12 px on cards, 999 px on pills and primary buttons.
- Focus ring: 3 px outline in the secondary colour, 2 px offset, on every interactive element.
- Touch targets at least 44 × 44 px.
- Day/Night: both modes ship as CSS variables, with a toggle and respect for the system setting.

## 4. Image brief (for you to generate with AI)

**Why images:** the data already points to image files, and the festival is a visual event. The prototype uses labelled gray boxes, so nothing here blocks Seminar 3.

**Rules for every image**
- No real or identifiable people: show people from behind, in silhouette, or softly out of focus. No celebrities.
- No text, logos, brand names or watermarks inside the image.
- Valencia beachfront or club feel, Mediterranean light, no landmark that identifies a real private venue.
- Check hands, faces and instruments for AI errors. Regenerate if wrong.
- After each image, add a row to `docs/image-prompts.md` (file, tool, prompt, date) and keep the `alt` text in `data.json`.

**Style block (paste at the start of every photo prompt)**
> Warm golden-hour editorial photography, natural film grain, soft sunset light, Mediterranean beachfront in Valencia, Spain. Candid and joyful. Diverse adults dancing bachata, seen from behind, in silhouette, or with faces softly out of focus so nobody is identifiable. No text, no logos, no watermarks.

### Priority 1 (needed for the build)
| # | File (path in the data) | Size and ratio | What to show |
|---|---|---|---|
| 1 | `hero-day.jpg` | 2400 × 1350, 16:9 | Dancers on a sand dance floor at golden hour, sea in the background |
| 2 | `hero-night.jpg` | 2400 × 1350, 16:9 | Indoor club floor, warm amber light, crowd in silhouette |
| 3 | `images/venues/arena-stage.jpg` | 1600 × 1200, 4:3 | A sand-floor open-air stage on a beachfront at sunset |
| 4 | `images/venues/pabellon-brisa.jpg` | 1600 × 1200, 4:3 | Bright seaside pavilion, sprung wooden floor, sea-view windows, workshop in progress |
| 5 | `images/venues/marea-club.jpg` | 1600 × 1200, 4:3 | Night club dance floor, stage, bar, warm light |
| 6 | `og-image.jpg` | 1200 × 630, 1.91:1 | Brand image: sunset over the sea with dancers' silhouettes, empty space on the left for a title added later |
| 7 | 8 featured performer images (`images/performers/<slug>.jpg`) | 800 × 800, 1:1 | See list below |
| 8 | 5 instrument illustrations for Roots | 800 × 800, 1:1 | Flat vector-style illustrations of requinto guitar, segunda guitar, bongo, güira, bass, in the chosen palette |

**Featured performers (item 7)**
- `marisol-and-tavo`: a dance couple in a teaching pose, seen from behind or cropped at the shoulders
- `noelia-and-bruno`: a couple in casual dance wear on a beachfront promenade, faces out of focus
- `yara-and-elias`: a couple, with a man holding an acoustic guitar, faces out of focus
- `dj-soledad-rey`: a DJ at a booth with old cassette tapes on the table, from behind
- `dj-hugo-tamarit`: a DJ at a beach bar booth at sunset, silhouette
- `cuarteto-salitre`: a four-piece band with guitar, bongo, güira and bass on a small stage, silhouettes
- `ola-brava-dance-company`: an eight-dancer troupe in a stage pose, silhouettes
- `raiz-viva-ensemble`: a ten-dancer ensemble in a circle, silhouettes

### Priority 2 (the other 56 performers)
Generating 56 portraits is a lot. My recommendation: **12 illustrated avatars** (4 types × 3 colour variants: instructor, DJ, band or singer, show team) reused across performers. This would change the image paths for those 56 performers in `data.json`, which is a small data change that we would justify in the log. The alternative is 56 individual images.

### Prompt template for each image
> [Style block] Subject: [what to show]. Composition: [wide / medium / close], [camera height], [space left for text if needed]. Aspect ratio [16:9 / 4:3 / 1:1]. Quality: sharp, high resolution.

## 5. Decisions needed
1. Palette: A, B or C.
2. Font pair: 1 or 2.
3. Performer images: 12 illustrated avatars (recommended) or 56 individual images.
4. Which images you will generate first (start with 1, 3, 4 and 5).
