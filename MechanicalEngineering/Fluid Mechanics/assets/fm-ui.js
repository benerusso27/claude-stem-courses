/* ENGR/EGTG 4254 Fluid Mechanics study guides: shared page behavior.
   Theme toggle, contents highlighting, self-check questions, number inputs, and a small SVG plotting helper.
   Every page loads fm-core.js first, then this file, then its own script. */
(function () {
  'use strict';
  const C = window.FMC;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const NS = 'http://www.w3.org/2000/svg';

  /* ---------- theme (per-viewer convenience; storage may be unavailable) ---------- */
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } return null; }
  function applyTheme(t) { if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t); else document.documentElement.removeAttribute('data-theme'); }
  applyTheme(store('fm-theme'));
  function themeButton() {
    const b = $('#themebtn'); if (!b) return;
    const label = () => { const t = document.documentElement.getAttribute('data-theme'); b.textContent = t === 'dark' ? 'Dark' : t === 'light' ? 'Light' : 'Auto'; };
    label();
    b.addEventListener('click', () => {
      const t = document.documentElement.getAttribute('data-theme');
      const next = t === null ? 'light' : t === 'light' ? 'dark' : 'auto';
      applyTheme(next); store('fm-theme', next); label();
      document.dispatchEvent(new CustomEvent('fm-theme'));
    });
  }

  /* ---------- contents highlighting ---------- */
  function tocSpy() {
    const links = $$('.toc a[href^="#"]'); if (!links.length || !('IntersectionObserver' in window)) return;
    const map = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
    const io = new IntersectionObserver((ents) => {
      ents.forEach((e) => { if (e.isIntersecting) { links.forEach((l) => l.classList.remove('on')); const a = map.get(e.target.id); if (a) a.classList.add('on'); } });
    }, { rootMargin: '-15% 0px -75% 0px' });
    map.forEach((a, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }

  /* ---------- self-check multiple choice ---------- */
  // Markup: <div class="q" data-answer="b"><p class="qt">…</p><div class="opts"><button class="opt" data-k="a">…</button>…</div><p class="fb" hidden>…</p></div>
  function quizzes() {
    $$('.q').forEach((q) => {
      const ans = q.dataset.answer, fb = $('.fb', q);
      $$('button.opt', q).forEach((b) => b.addEventListener('click', () => {
        $$('button.opt', q).forEach((x) => x.classList.remove('right', 'wrong'));
        b.classList.add(b.dataset.k === ans ? 'right' : 'wrong');
        if (b.dataset.k !== ans) $(`button.opt[data-k="${ans}"]`, q).classList.add('right');
        if (fb) fb.hidden = false;
      }));
    });
  }

  /* ---------- inputs ---------- */
  const num = (el) => C.parseNum(typeof el === 'string' ? ($(el) || {}).value : el.value);
  function setVals(obj) { Object.entries(obj).forEach(([id, v]) => { const el = document.getElementById(id); if (el) el.value = v; }); }
  function onInputs(container, fn) {
    const root = typeof container === 'string' ? $(container) : container;
    root.addEventListener('input', fn); root.addEventListener('change', fn);
  }
  function segmented(group, fn) {
    const btns = $$('button', group);
    btns.forEach((b) => b.addEventListener('click', () => { btns.forEach((x) => x.setAttribute('aria-pressed', String(x === b))); fn(b.dataset.v, b); }));
  }
  function typeset(el) { if (window.MathJax && MathJax.typesetPromise) { MathJax.typesetPromise(el ? [el] : undefined).catch(() => {}); } }

  /* ---------- SVG helpers ---------- */
  function el(name, attrs, parent) {
    const e = document.createElementNS(NS, name);
    for (const k in attrs) if (attrs[k] !== undefined && attrs[k] !== null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function text(parent, x, y, s, attrs = {}) { const t = el('text', Object.assign({ x, y, 'font-size': 12, class: 'svg-ink2' }, attrs), parent); t.textContent = s; return t; }
  function niceTicks(lo, hi, n = 5) {
    const span = hi - lo; if (!(span > 0)) return [lo];
    const step0 = span / n, mag = Math.pow(10, Math.floor(Math.log10(step0)));
    const r = step0 / mag, step = (r < 1.5 ? 1 : r < 3 ? 2 : r < 7 ? 5 : 10) * mag;
    const out = []; for (let v = Math.ceil(lo / step - 1e-9) * step; v <= hi + step * 1e-9; v += step) out.push(Math.abs(v) < step * 1e-9 ? 0 : v);
    return out;
  }
  // plot(svg, {W,H, m:{l,r,t,b}, x:{min,max,log,label,ticks,fmt}, y:{...}, grid:true}) -> {sx, sy, g, box}
  function plot(svg, o) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    const W = o.W || 640, H = o.H || 380, m = Object.assign({ l: 62, r: 18, t: 16, b: 48 }, o.m || {});
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    const pw = W - m.l - m.r, ph = H - m.t - m.b;
    const mk = (ax, a0, a1) => ax.log
      ? (v) => a0 + (Math.log10(v) - Math.log10(ax.min)) / (Math.log10(ax.max) - Math.log10(ax.min)) * (a1 - a0)
      : (v) => a0 + (v - ax.min) / (ax.max - ax.min) * (a1 - a0);
    const sx = mk(o.x, m.l, m.l + pw), sy = mk(o.y, m.t + ph, m.t);
    const g = el('g', {}, svg);
    el('rect', { x: m.l, y: m.t, width: pw, height: ph, class: 'fl-surface' }, g);
    const ticks = (ax) => ax.ticks || (ax.log ? logTicks(ax.min, ax.max) : niceTicks(ax.min, ax.max, ax.n || 5));
    const fx = o.x.fmt || ((v) => C.fmt(v, 3)), fy = o.y.fmt || ((v) => C.fmt(v, 3));
    if (o.x.log && o.grid !== false) logMinor(o.x.min, o.x.max).forEach((v) => el('line', { x1: sx(v), x2: sx(v), y1: m.t, y2: m.t + ph, class: 'st-rule', 'stroke-width': 0.5, opacity: 0.6 }, g));
    if (o.y.log && o.grid !== false) logMinor(o.y.min, o.y.max).forEach((v) => el('line', { y1: sy(v), y2: sy(v), x1: m.l, x2: m.l + pw, class: 'st-rule', 'stroke-width': 0.5, opacity: 0.6 }, g));
    ticks(o.x).forEach((v) => { if (o.grid !== false) el('line', { x1: sx(v), x2: sx(v), y1: m.t, y2: m.t + ph, class: 'st-rule', 'stroke-width': 1 }, g); text(g, sx(v), m.t + ph + 17, fx(v), { 'text-anchor': 'middle', 'font-size': 11.5 }); });
    ticks(o.y).forEach((v) => { if (o.grid !== false) el('line', { y1: sy(v), y2: sy(v), x1: m.l, x2: m.l + pw, class: 'st-rule', 'stroke-width': 1 }, g); text(g, m.l - 7, sy(v) + 4, fy(v), { 'text-anchor': 'end', 'font-size': 11.5 }); });
    el('rect', { x: m.l, y: m.t, width: pw, height: ph, fill: 'none', class: 'st-ink2', 'stroke-width': 1 }, g);
    if (o.x.label) text(g, m.l + pw / 2, H - 8, o.x.label, { 'text-anchor': 'middle', 'font-size': 12.5, class: 'svg-ink' });
    if (o.y.label) text(g, 14, m.t + ph / 2, o.y.label, { 'text-anchor': 'middle', 'font-size': 12.5, class: 'svg-ink', transform: `rotate(-90 14 ${m.t + ph / 2})` });
    const clipId = 'c' + Math.random().toString(36).slice(2, 8);
    const cp = el('clipPath', { id: clipId }, el('defs', {}, svg)); el('rect', { x: m.l, y: m.t, width: pw, height: ph }, cp);
    const inner = el('g', { 'clip-path': `url(#${clipId})` }, svg);
    return { sx, sy, g: inner, axes: g, box: { l: m.l, t: m.t, w: pw, h: ph, W, H } };
  }
  function logTicks(a, b) { const out = []; for (let e = Math.ceil(Math.log10(a) - 1e-9); e <= Math.floor(Math.log10(b) + 1e-9); e++) out.push(Math.pow(10, e)); return out; }
  function logMinor(a, b) { const out = []; for (let e = Math.floor(Math.log10(a)); e <= Math.ceil(Math.log10(b)); e++) for (let k = 2; k <= 9; k++) { const v = k * Math.pow(10, e); if (v > a && v < b) out.push(v); } return out; }
  function line(p, pts, attrs = {}) {
    const d = pts.filter((q) => isFinite(q[0]) && isFinite(q[1])).map((q, i) => `${i ? 'L' : 'M'}${p.sx(q[0]).toFixed(2)},${p.sy(q[1]).toFixed(2)}`).join('');
    return el('path', Object.assign({ d, fill: 'none', 'stroke-width': 2.2, class: 'st-water', 'stroke-linejoin': 'round' }, attrs), p.g);
  }
  function dot(p, x, y, attrs = {}) { return el('circle', Object.assign({ cx: p.sx(x), cy: p.sy(y), r: 5, class: 'fl-dye' }, attrs), p.g); }
  // Arrow marker defs (call once per svg): returns marker id for the given class.
  function arrowDef(svg, cls, id) {
    let defs = svg.querySelector('defs'); if (!defs) defs = el('defs', {}, svg);
    const mk = el('marker', { id, viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' }, defs);
    el('path', { d: 'M0,0 L10,5 L0,10 z', class: cls }, mk);
    return `url(#${id})`;
  }

  /* ---------- page start ---------- */
  function present() {
    const b = $('.presbtn'); if (!b) return;
    const set = (on) => { if (on) document.documentElement.setAttribute('data-present', ''); else document.documentElement.removeAttribute('data-present'); b.setAttribute('aria-pressed', String(on)); store('fm-present', on ? '1' : '0'); document.dispatchEvent(new CustomEvent('fm-theme')); };
    set(store('fm-present') === '1');
    b.addEventListener('click', () => set(!document.documentElement.hasAttribute('data-present')));
    document.addEventListener('keydown', (e) => { if (e.key === 'p' && e.altKey) set(!document.documentElement.hasAttribute('data-present')); });
  }
  function start() { themeButton(); present(); tocSpy(); quizzes(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();

  window.FM = { $, $$, num, setVals, onInputs, segmented, typeset, el, text, plot, line, dot, arrowDef, niceTicks, logTicks, store };
})();
