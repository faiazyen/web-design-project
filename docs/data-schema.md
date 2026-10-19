# data.json schema proposal (Step 1.4)

**Status:** APPROVED by Faiaz (A) on 2026-10-19, with 3 venues and the 64-performer mix. Amended once after the first validator run: a programme day runs from 06:00 to 06:00 (see Global rules). Data generated and validated.

Source of truth: `data.json` at the repo root. `scripts/build-data.py` converts it into `web/js/data.js` as `window.FESTIVAL_DATA = {...};`.

## Global rules

- **Ids:** stable strings. `ven-001`…, `perf-001`…, `item-001`…, `day-fri|day-sat|day-sun`. Never reused.
- **Slugs:** lowercase ASCII, hyphens, unique inside their entity. Used in `?slug=` detail URLs.
- **Time:** ISO 8601 with offset, e.g. `2027-06-26T11:00:00+02:00`. Timezone `Europe/Madrid`, which is UTC+02:00 in June 2027. (The brief's prompt mentions Europe/Prague because it assumes a Czech festival. Ours is in Valencia, and both are UTC+02:00 in June.)
- **Programme day:** a programme day runs from 06:00 to 06:00. A set that starts at 01:30 on Saturday morning belongs to **Friday** night (`dayId = day-fri`). Every item starts between 2027-06-25 06:00 and 2027-06-28 05:59 and ends no later than 06:00 the morning after its programme day.
- **Fictional:** every person, band, venue and organisation is invented. No name may match a well-known real bachata artist.
- **Images:** every image object has `src`, `alt`, `credit`, `source` (AI-generated or free licence).
- **Derived, not stored:** a performer's sessions, a venue's sessions, and `dayPart` consistency are derived from `programmeItems`.

## Top level

| Key | Type | Required | Notes |
|---|---|---|---|
| `festival` | object | yes | One record |
| `days` | array of day | yes | Exactly 3 |
| `categories` | object | yes | Lookup lists for filters and quiz |
| `venues` | array of venue | yes | 3 records (minimum 2) |
| `performers` | array of performer | yes | 64 records |
| `programmeItems` | array of item | yes | 72 records |

## festival

| Field | Type | Req | Notes |
|---|---|---|---|
| `id` | string | yes | `fest-2027` |
| `slug` | string | yes | |
| `name` | string | yes | Latino Mar Bachata Festival |
| `edition` | integer | yes | 1 |
| `editionLabel` | string | yes | "1st edition · Primera Ola" |
| `year` | integer | yes | 2027 |
| `startDate`, `endDate` | date | yes | 2027-06-25, 2027-06-27 |
| `timezone` | string | yes | Europe/Madrid |
| `city`, `country`, `countryCode` | string | yes | Valencia, Spain, ES |
| `tagline`, `description` | string | yes | |
| `themes[]`, `genres[]` | string[] | yes | |
| `language`, `currency` | string | yes | en, EUR |
| `contact` | object | yes | `email` (reserved `.example` domain) |
| `tickets[]` | object[] | yes | `id`, `name`, `price`, `currency`, `includes[]`, `notes` |
| `accommodation[]` | object[] | yes | `id`, `name`, `type`, `distanceToVenuesKm`, `priceFromPerNight`, `notes` |
| `travel[]` | object[] | yes | `id`, `mode`, `title`, `text` |
| `faq[]` | object[] | yes | `id`, `topic`, `question`, `answer` |
| `codeOfConduct` | object | yes | `summary`, `principles[]`, `reportContact` |
| `accessibility` | object | yes | `summary`, `features[]` |
| `sustainability` | object | yes | `summary`, `commitments[]` |
| `roots` | object | yes | `intro`, `timeline[{year, text}]`, `instruments[{name, text}]` |

## day

`id`, `date`, `label`, `theme`.

## categories

`types[]`, `levels[]`, `roleFocus[]`, `styles[]`, `performerTypes[]`, `dayParts[]`. Each entry is `{ "id": "...", "label": "...", "description": "..." }`. `description` is required for `levels` (used by the level quiz).

## venue

| Field | Type | Req | Notes |
|---|---|---|---|
| `id`, `slug`, `name` | string | yes | |
| `kind` | enum | yes | `beach-stage`, `pavilion`, `club` |
| `setting` | enum | yes | `outdoor`, `indoor` |
| `description` | string | yes | |
| `address` | object | yes | `streetAddress`, `postalCode`, `addressLocality`, `addressRegion`, `addressCountry` (maps to schema.org `PostalAddress`) |
| `geo` | object | yes | `latitude`, `longitude` |
| `capacity` | integer | yes | |
| `accessibility` | object | yes | `stepFree`, `accessibleToilets`, `quietSpace` (booleans), `notes` |
| `mapZone` | string | yes | id of the SVG zone on the venue map |
| `image` | object | yes | image rules above |

## performer

| Field | Type | Req | Notes |
|---|---|---|---|
| `id`, `slug`, `name` | string | yes | |
| `type` | enum | yes | `instructor`, `dj`, `band`, `singer`, `show-team` |
| `members[]` | string[] | no | Couples and teams |
| `country` | string | yes | ISO 3166-1 alpha-2 |
| `styles[]` | string[] | yes | from `categories.styles` |
| `bio` | string | yes | |
| `featured` | boolean | yes | Used on Home |
| `image` | object | yes | image rules above |

## programmeItem

| Field | Type | Req | Notes |
|---|---|---|---|
| `id`, `slug`, `title` | string | yes | |
| `type` | enum | yes | `workshop`, `show`, `social` |
| `level` | enum | yes | `beginner`, `intermediate`, `advanced`, `all-levels` (shows and socials use `all-levels`) |
| `roleFocus` | enum | yes | `lead`, `follow`, `both` |
| `style` | enum | yes | from `categories.styles` |
| `dayId` | string | yes | the programme day of `start` (start minus 6 hours gives its date) |
| `start`, `end` | datetime | yes | ISO 8601 with offset, `end` after `start` |
| `dayPart` | enum | yes | `night` if `start` is 20:00 or later, or before 06:00. Otherwise `day`. |
| `venueId` | string | yes | → `venues.id` |
| `performerIds[]` | string[] | yes | → `performers.id`, at least one |
| `description` | string | yes | |
| `capacity` | integer or null | yes | null for open events |
| `tags[]` | string[] | no | search terms |

## Example records

**festival** (shortened)

```json
{
  "id": "fest-2027",
  "slug": "latino-mar-bachata-festival-2027",
  "name": "Latino Mar Bachata Festival",
  "edition": 1,
  "editionLabel": "1st edition · Primera Ola",
  "year": 2027,
  "startDate": "2027-06-25",
  "endDate": "2027-06-27",
  "timezone": "Europe/Madrid",
  "city": "Valencia",
  "country": "Spain",
  "countryCode": "ES",
  "tagline": "Sea by day, club by night.",
  "themes": ["the sea", "roots of bachata dominicana"],
  "genres": ["bachata dominicana", "bachata sensual", "bachata moderna", "salsa"],
  "language": "en",
  "currency": "EUR",
  "contact": { "email": "info@latinomar.example" },
  "tickets": [
    { "id": "tick-full", "name": "Full Pass", "price": 149, "currency": "EUR",
      "includes": ["All workshops", "All socials", "All shows"], "notes": "Three days." }
  ],
  "faq": [
    { "id": "faq-001", "topic": "levels", "question": "Which workshop level should I pick?",
      "answer": "Pick beginner if you have danced bachata fewer than 10 times." }
  ]
}
```

**day**

```json
{ "id": "day-sat", "date": "2027-06-26", "label": "Saturday", "theme": "Sunset on the sand" }
```

**category** (levels entry)

```json
{ "id": "beginner", "label": "Beginner",
  "description": "You know the basic step and can dance a full song with a partner." }
```

**venue**

```json
{
  "id": "ven-001",
  "slug": "arena-stage",
  "name": "Arena Stage",
  "kind": "beach-stage",
  "setting": "outdoor",
  "description": "Sand-floor stage on the beachfront for the daytime socials and sunset sessions.",
  "address": {
    "streetAddress": "Passeig de la Ola 1",
    "postalCode": "46011",
    "addressLocality": "Valencia",
    "addressRegion": "Comunitat Valenciana",
    "addressCountry": "ES"
  },
  "geo": { "latitude": 39.4775, "longitude": -0.3250 },
  "capacity": 800,
  "accessibility": {
    "stepFree": true,
    "accessibleToilets": true,
    "quietSpace": false,
    "notes": "Firm boardwalk path from the promenade to the dance floor."
  },
  "mapZone": "zone-arena",
  "image": { "src": "images/venue-arena-stage.jpg", "alt": "Dancers on a sand dance floor at sunset",
             "credit": "AI-generated", "source": "image model, prompt in docs/" }
}
```

**performer**

```json
{
  "id": "perf-001",
  "slug": "marisol-and-tavo",
  "name": "Marisol & Tavo",
  "type": "instructor",
  "members": ["Marisol Vega", "Tavo Reyes"],
  "country": "DO",
  "styles": ["dominicana", "sensual"],
  "bio": "Instructor couple from Santo Domingo who teach the footwork of traditional bachata.",
  "featured": true,
  "image": { "src": "images/perf-001.jpg", "alt": "A dance couple smiling in a studio",
             "credit": "AI-generated", "source": "image model, prompt in docs/" }
}
```

**programmeItem**

```json
{
  "id": "item-001",
  "slug": "beginner-bachata-basics-follow",
  "title": "Bachata basics: the follower's step",
  "type": "workshop",
  "level": "beginner",
  "roleFocus": "follow",
  "style": "dominicana",
  "dayId": "day-sat",
  "start": "2027-06-26T11:00:00+02:00",
  "end": "2027-06-26T12:15:00+02:00",
  "dayPart": "day",
  "venueId": "ven-002",
  "performerIds": ["perf-001"],
  "description": "Learn the basic step, the hip movement and how to follow a lead.",
  "capacity": 60,
  "tags": ["basics", "footwork"]
}
```

## Self-check: can the spec be answered from these fields?

| Spec item | Fields used | OK |
|---|---|---|
| Filter by day | `programmeItems.dayId` | yes |
| Filter by venue | `programmeItems.venueId` | yes |
| Filter by type | `programmeItems.type` | yes |
| Filter by level | `programmeItems.level` | yes |
| Filter by role focus | `programmeItems.roleFocus` | yes |
| Filter by Day/Night | `programmeItems.dayPart` | yes |
| Clash warning in My Programme | `start`, `end` | yes |
| Calendar download | `title`, `start`, `end`, `venues.name`, `address` | yes |
| Search | `title`, `description`, `tags`, `performers.name`, `venues.name`, `faq`, `roots` | yes |
| Performer page with all sessions | derived from `performerIds` | yes |
| Venue page with all sessions | derived from `venueId` | yes |
| Level quiz | `categories.levels.description` and item `level` | yes |
| Venue map | `venues.mapZone` | yes |
| Access facts | `venues.accessibility`, `festival.accessibility` | yes |
| Tickets, accommodation, travel, FAQ, code of conduct | `festival.*` | yes |
| JSON-LD Festival, Event, Place, Person, Breadcrumb, FAQ | all of the above | yes |
| Scenario 1 (beginner follower on Saturday) | `dayId`, `type`, `level`, `roleFocus`, `start`, `end` | yes |
| Scenario 2 (DJ tonight, end time) | `type=social`, `dayPart`, `performerIds`, `end`, `performers.type=dj` | yes |
| Scenario 3 (search an instructor) | `performers.name`, derived sessions | yes |

## Decisions on the open questions

1. Schema approved as written, then amended once (programme-day rule above).
2. Three venues: Arena Stage (beach), Pabellón Brisa (pavilion), Marea Club (club).
3. Performer mix for 64: 22 instructors, 14 DJs, 6 bands, 6 singers, 16 show teams.
