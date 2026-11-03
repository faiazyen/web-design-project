# Prototype verification record (Seminar 3)

Date: 2026-11-03. Tester: Claude Code, driving a real browser (the app's built-in browser), first with the prototype on a local test server (`http://localhost:8765`) and later on the live site. Viewports: 320 px, 375 px (phone) and 1280 px (desktop).

## 1. Scenario 1: first-timer, beginner follower (phone, 375 px)
| Step | Result |
|---|---|
| Open Programme with Day = Saturday, Type = Workshop, Level = Beginner, Role = Follow | "Showing 4 of 65 sessions" (09:30 and 11:00 workshops in two venues). On a phone the filter panel folds, so the list is visible at once. |
| Press Save on "Saturday starter: the follower's basics" while logged out | Sent to Log in / Sign up with the reason shown. The pending save is remembered. |
| Sign up with name, email, demo password | Returned to the same filtered Programme. The first workshop is saved, a message says so, and the header shows "Hi, Lucia". |
| Press Save on "Saturday starter: body movement basics" | Saved. |
| Open My Programme | Two sessions listed under Saturday 26 June, banner "No clashes". |
| Extra: save "Morning basics by the sea" (09:30, overlaps) | Banner "Clash: 2 of your sessions overlap" and a text warning on both sessions. Removing it clears the warning. |
| Check storage | The password is not stored. Saved ids are kept under the account. |

## 2. Scenario 2: experienced dancer, evening (desktop, 1280 px)
| Step | Result |
|---|---|
| Programme filtered to Friday, Social, Night, Marea Club | 4 sessions: 22:00 (DJ Tarek Noor and Yeral Bonilla), and three sets after midnight shown as "Fri night ... (after midnight)". |
| Open the 22:00 session | Page shows time 22:00–23:30, venue, level, role, and links to both performers. |
| Open DJ Tarek Noor | Performer page lists all his sessions with times (Friday 22:00–23:30 and Sunday 21:15–22:45). |

## 3. Other checks
- Scenario 3 (not required, checked anyway): search "marisol" finds the instructor and three sessions; search "raiz" finds "Raíz" (accents ignored, match highlighted).
- Scenario 6: log out, wrong email gives "No account in this browser", log in with the right email (capital letters ignored) restores both saved sessions.
- Phone menu: opens with Menu, `aria-expanded` changes, Escape closes it and returns focus to the button.
- Automated page audit (11 pages at 320 px, 7 pages at 1280 px): one h1 per page, no skipped heading levels, every input has a label, every button has a name, no horizontal overflow, touch targets at least 44 px, title and description on every page, no duplicate ids.
- No network requests: the code and styles contain no `http`, `fetch` or `XMLHttpRequest` (checked by search).

## 4. Problems found by testing, and fixed
1. A pending Save was deleted when the login page loaded, so the first workshop was not saved after sign-up. Fixed: the pending save is only used once the visitor is logged in.
2. The performers list jumped from h1 to h3. Fixed with an h2.
3. "Filters (4 active)" had no space in the panel title. Fixed.
4. Sets after midnight read "Fri 00:00", which looks like the start of Friday. Now "Fri night 00:00–01:30 (after midnight)".
5. On a phone the six filters filled a whole screen before the results. Now two columns, and the panel folds when filters are already set.

## 5. Hosting and offline opening (added 2026-11-03)
- **Live site:** https://faiazyen.github.io/web-design-project/prototype/ (free GitHub Pages, public, HTTPS). Every key file answers 200 with the right type. Scenario 1 (phone, 375 px) and Scenario 2 (desktop, 1280 px) were run again on the live site: same results as above, no layout overflow, storage works.
- **Double-click (`file://`) in real Chrome:** the main pages (Home, Programme with the two scenario filters, a performer page, Search, Login, My Programme, the guide, Venues) were opened from local files. Each renders the header, the h1 and the results (for example "Showing 4 of 65 sessions"), and the "browser blocks storage" warning does not appear.
- **Calendar file:** the My Programme download builds valid calendar text: 2 events, correct UTC times (09:30 Madrid time shows as 07:30Z), commas escaped, ends with END:VCALENDAR.
- **Venues page** (added after the first test round): 3 venue cards with address, access facts and a link to each venue's sessions (Arena Stage links to 25 sessions).

## 6. Not verified
- Safari and Firefox (only Chrome was used for the file test).
- Screen readers, tablets, and a real user test.
- Opening the downloaded calendar file in a calendar app.
