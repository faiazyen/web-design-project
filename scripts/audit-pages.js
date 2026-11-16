/* Page audit. Run in a browser console (or the preview pane) on any page of the site served over http, for example
   http://localhost:8765/web/index.html . It loads every page listed in sitemap.xml plus the unlisted ones into a hidden iframe
   of a given width and checks: one h1, no skipped heading levels, labelled form controls, no horizontal overflow,
   touch targets of at least 44 px, images with alt, JSON-LD that parses, title, description, canonical, Open Graph,
   no external requests. Result: window.__audit = {width, pages, problems:[...]}. */
window.runAudit = async function (width, onlyPrefix) {
  const base = location.href.replace(/\/web\/.*$/, "/web/");
  const xml = await (await fetch(base + "sitemap.xml")).text();
  let urls = [...xml.matchAll(/<loc>[^<]*\/web\/([^<]*)<\/loc>/g)].map(m => m[1] || "index.html");
  urls = urls.concat(["my-programme.html", "login.html"]).filter((u, i, a) => a.indexOf(u) === i);
  if (onlyPrefix) urls = urls.filter(u => u.startsWith(onlyPrefix));
  const problems = [];
  const f = document.createElement("iframe");
  f.style.cssText = "position:fixed;left:0;top:0;width:" + width + "px;height:900px;border:0;visibility:hidden";
  document.body.appendChild(f);
  for (const u of urls) {
    await new Promise(r => { f.onload = r; f.src = base + u; });
    await new Promise(r => setTimeout(r, 60));
    const d = f.contentDocument, w = f.contentWindow, p = m => problems.push(u + ": " + m);
    const h1 = d.querySelectorAll("h1"); if (h1.length !== 1) p("h1 count " + h1.length);
    let last = 0; d.querySelectorAll("h1,h2,h3,h4,h5,h6").forEach(h => { const n = +h.tagName[1]; if (last && n > last + 1) p("heading skip to " + h.tagName + " '" + h.textContent.trim().slice(0, 30) + "'"); last = n; });
    d.querySelectorAll("input:not([type=hidden]),select,textarea").forEach(i => { const ok = i.labels && i.labels.length || i.getAttribute("aria-label"); if (!ok) p("unlabelled control " + (i.id || i.name)); });
    if (d.documentElement.scrollWidth > width) p("horizontal overflow " + d.documentElement.scrollWidth + " > " + width);
    d.querySelectorAll("a,button,input,select,summary").forEach(e => {
      if (e.hidden || e.type === "hidden" || e.closest("[hidden]") || e.classList.contains("skip-link")) return;
      const r = e.getBoundingClientRect(); if (!r.width || !r.height) return;
      const cs = w.getComputedStyle(e);
      if (cs.display === "inline" && e.tagName === "A" && e.closest("p,li,dd,td,address,h1,h2,h3,span,small")) return; // links in running text
      if (r.height < 43.5 || r.width < 43.5) p("small target " + e.tagName + " '" + (e.textContent || e.name || "").trim().slice(0, 24) + "' " + Math.round(r.width) + "x" + Math.round(r.height));
    });
    d.querySelectorAll("img").forEach(i => { if (!i.hasAttribute("alt")) p("img without alt " + i.getAttribute("src")); });
    d.querySelectorAll('script[type="application/ld+json"]').forEach(s => { try { JSON.parse(s.textContent); } catch (e) { p("bad JSON-LD"); } });
    if (!d.title || d.title.length < 10) p("title");
    const md = d.querySelector('meta[name=description]'); if (!md || md.content.length < 50) p("description");
    if (!d.querySelector('link[rel=canonical]')) p("canonical");
    ["og:title", "og:description", "og:image", "og:url"].forEach(k => { if (!d.querySelector('meta[property="' + k + '"]')) p("missing " + k); });
    if (!d.querySelector("main#main") || !d.querySelector(".skip-link") || d.documentElement.lang !== "en") p("landmarks/lang");
    const sm = [...d.querySelectorAll("body *")].filter(e => e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && parseFloat(w.getComputedStyle(e).fontSize) < 13.9 && !e.closest("script,style")); if (sm.length) p("text under 14px: " + sm[0].tagName);
    d.querySelectorAll("a[href]").forEach(a => { const h = a.getAttribute("href"); if (/^https?:/.test(h) && !h.startsWith(location.origin)) p("external link " + h); });
  }
  f.remove();
  window.__audit = { width, pages: urls.length, problems };
  return window.__audit;
};
