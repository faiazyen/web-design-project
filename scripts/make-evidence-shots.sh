#!/bin/bash
# Screenshots of the real site (web/) opened from file:// in headless Chrome, for docs/evidence and the slides.
# Phone (375 px) shots are taken in the browser pane, because headless Chrome has a minimum window width of 500 px.
# Night shots use Chrome's dark mode, so they also prove that the site follows the system setting.
cd "$(dirname "$0")/.." || exit 1
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; B="file://$PWD/web"
shot(){ "$C" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=3000 --window-size=$2 $4 --screenshot="$PWD/docs/evidence/$1.png" "$3" >/dev/null 2>&1; }
shot web-home-desktop-day 1280,860 "$B/index.html"
shot web-home-desktop-night 1280,860 "$B/index.html" --force-dark-mode
shot web-programme-desktop 1280,860 "$B/programme.html?day=day-fri&venue=ven-003&type=social&daypart=night"
shot web-session-desktop 1280,860 "$B/sessions/club-night-dj-tarek-noor-fri.html"
shot web-performers-desktop 1280,860 "$B/performers.html"
ls docs/evidence/web-*.png
