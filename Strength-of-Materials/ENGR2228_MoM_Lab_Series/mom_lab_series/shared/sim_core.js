/* SimCore — shared by every simulation in the ENGR 2228 lab series (inlined at build time).
   No dependencies; works offline. Provides: unit system (SI primary, US toggle), number
   formatting, slider controls, an SVG plotter with hover readout, CSV export with a
   copy-to-clipboard fallback. Physics never lives here: each lab keeps its model in a
   <script id="model"> block of pure functions so the Node tests load exactly what runs. */
const SimCore = (() => {
  'use strict';
  const KSI = 6.894757293168e6, IN = 0.0254, LBF = 4.4482216152605;
  // quantity -> [factor from SI base, label] per unit system
  const Q = {
    stress:     { SI: [1e-6, 'MPa'],   US: [1 / KSI, 'ksi'] },
    modulus:    { SI: [1e-9, 'GPa'],   US: [1 / KSI, 'ksi'] },
    length:     { SI: [1e3, 'mm'],     US: [1 / IN, 'in'] },
    longlength: { SI: [1, 'm'],        US: [1 / (12 * IN), 'ft'] },
    force:      { SI: [1e-3, 'kN'],    US: [1 / (1000 * LBF), 'kip'] },
    compliance: { SI: [1e6, 'mm/kN'],  US: [1000 * LBF / IN, 'in/kip'] },
    energy:     { SI: [1e-6, 'MJ/m³'], US: [1000 / KSI, 'in·lb/in³'] },
    area:       { SI: [1e6, 'mm²'],    US: [1 / (IN * IN), 'in²'] },
    moment:     { SI: [1, 'N·m'],      US: [1 / (LBF * IN), 'lb·in'] },
    angle:      { SI: [180 / Math.PI, '°'], US: [180 / Math.PI, '°'] },
    twistrate:  { SI: [180 / Math.PI, '°/m'], US: [180 / Math.PI / 3.280839895, '°/ft'] },
    inertia:    { SI: [1e12, 'mm⁴'],   US: [1 / IN ** 4, 'in⁴'] },
    volume3:    { SI: [1e9, 'mm³'],    US: [1 / IN ** 3, 'in³'] },
    power:      { SI: [1e-3, 'kW'],    US: [1 / 745.69987, 'hp'] },
    temperature:{ SI: [1, '°C'],       US: [1.8, '°F'] },
    percent:    { SI: [100, '%'],      US: [100, '%'] },
    shearflow:  { SI: [1e-3, 'N/mm'],  US: [IN / LBF, 'lb/in'] },
    stiffness:  { SI: [1e-6, 'kN/mm'], US: [IN / (1000 * LBF), 'kip/in'] },
    rigidity:   { SI: [1, 'N·m²'],     US: [1 / (LBF * IN * IN), 'lb·in²'] },
    forceN:     { SI: [1, 'N'],        US: [1 / LBF, 'lbf'] },
    rotstiff:   { SI: [1, 'N·m/rad'],  US: [1 / (LBF * IN), 'lb·in/rad'] },
    lineload:   { SI: [1e-3, 'kN/m'],  US: [0.3048 / (1000 * LBF), 'kip/ft'] },
    microstrain:{ SI: [1e6, 'µε'],     US: [1e6, 'µε'] },
    pressure:   { SI: [1e-6, 'MPa'],   US: [1 / 6894.757293168, 'psi'] },
    none:       { SI: [1, ''],         US: [1, ''] },
  };
  let system = 'SI';
  const listeners = [];
  const setSystem = (s) => { system = s; listeners.forEach((f) => f(s)); };
  const onSystem = (f) => listeners.push(f);
  const getSystem = () => system;
  const conv = (q, v) => v * Q[q][system][0];
  const unconv = (q, v) => v / Q[q][system][0];
  const unit = (q) => Q[q][system][1];
  const csvUnit = (q) => unit(q).replace('µε', 'ue').replace('²', '2').replace('³', '3').replace('⁴', '4').replace('·', '').replace('°', 'deg').replace('/', '_per_').replace('%', 'pct');

  const SUP = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' };
  function fmt(v, sig = 4) {
    if (v === null || v === undefined || !Number.isFinite(v)) return '—';
    if (v === 0) return '0';
    const a = Math.abs(v);
    if (a >= 1e6 || a < 1e-4) {
      const [m, e] = v.toExponential(sig - 1).split('e');
      return m.replace('-', '−') + '×10' + String(parseInt(e, 10)).split('').map((c) => SUP[c] || c).join('');
    }
    const digits = Math.floor(Math.log10(a)) + 1;
    const dec = Math.max(0, sig - digits);
    let s = (Math.round(v * 10 ** dec) / 10 ** dec).toFixed(dec);
    const [ip, fp] = s.replace('-', '').split('.');
    const ipg = ip.length > 4 ? ip.replace(/\B(?=(\d{3})+(?!\d))/g, ' ') : ip;
    return (v < 0 ? '−' : '') + ipg + (fp !== undefined ? '.' + fp : '');
  }
  const fmtQ = (q, v, sig = 4) => fmt(conv(q, v), sig) + (unit(q) ? ' ' + unit(q) : '');
  const plain = (v, sig = 8) => (Number.isFinite(v) ? Number(v.toPrecision(sig)).toString() : '');

  // ---------------------------------------------------------------- controls
  function el(tag, attrs = {}, html = '') {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (html) e.innerHTML = html;
    return e;
  }
  /* spec: {id, label, sym(html), q, min, max, step, log, int, sig, help}
     values are SI internally; the number box shows/accepts the active unit system. */
  function slider(container, spec, value, onChange) {
    const q = spec.q || 'none';
    const wrap = el('div', { class: 'ctl' });
    const lab = el('label', { for: spec.id + '-num' }, `<span class="sym">${spec.sym || ''}</span><span>${spec.label}</span>`);
    const row = el('div', { class: 'ctl-row' });
    const r = el('input', { type: 'range', id: spec.id, min: 0, max: 1000, step: 1, 'aria-label': spec.label });
    const nbox = el('input', { type: 'number', id: spec.id + '-num', inputmode: 'decimal', step: 'any' });
    const u = el('span', { class: 'unit' });
    row.append(r, nbox, u);
    wrap.append(lab, row);
    if (spec.help) wrap.append(el('p', { class: 'help', id: spec.id + '-help' }, spec.help));
    container.append(wrap);
    let v = value;
    const toPos = (x) => spec.log ? 1000 * Math.log(x / spec.min) / Math.log(spec.max / spec.min) : 1000 * (x - spec.min) / (spec.max - spec.min);
    const fromPos = (p) => {
      let x = spec.log ? spec.min * Math.pow(spec.max / spec.min, p / 1000) : spec.min + (spec.max - spec.min) * p / 1000;
      if (spec.int) x = Math.round(x);
      else if (spec.step) x = Math.round(x / spec.step) * spec.step;
      return Math.min(spec.max, Math.max(spec.min, x));
    };
    const show = () => {
      r.value = String(Math.round(toPos(v)));
      const shown = conv(q, v);
      nbox.value = spec.int ? String(Math.round(shown)) : String(Number(shown.toPrecision(spec.sig || 4)));
      u.textContent = unit(q);
      r.setAttribute('aria-valuetext', `${nbox.value} ${unit(q)}`.trim());
    };
    r.addEventListener('input', () => { v = fromPos(+r.value); show(); onChange(v); });
    nbox.addEventListener('change', () => {
      const x = parseFloat(nbox.value);
      if (!Number.isFinite(x)) { show(); return; }
      v = Math.min(spec.max, Math.max(spec.min, unconv(q, x)));
      if (spec.int) v = Math.round(v);
      show(); onChange(v);
    });
    onSystem(show);
    show();
    return { set: (x) => { v = x; show(); }, get: () => v, el: wrap, range: r, box: nbox };
  }

  function segmented(container, options, value, onChange, label) {
    const g = el('div', { class: 'seg', role: 'group', 'aria-label': label || '' });
    const btns = options.map(([val, text]) => {
      const b = el('button', { type: 'button', 'aria-pressed': String(val === value), 'data-v': val }, text);
      b.addEventListener('click', () => { btns.forEach((x) => x.setAttribute('aria-pressed', String(x === b))); onChange(val); });
      g.append(b);
      return b;
    });
    container.append(g);
    return { set: (val) => btns.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.v === val))) };
  }

  // ---------------------------------------------------------------- CSV export
  function toCSV(header, rows) {
    const esc = (x) => { const s = String(x); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
    return [header.map(esc).join(','), ...rows.map((r) => r.map(esc).join(','))].join('\n') + '\n';
  }
  /* Saves the CSV and always also shows it in `panel` (a <details> with a textarea and a Copy
     button). Hosted on claude.ai the page asks the viewer through the `downloads` capability (the
     viewer confirms each save); opened as a local file it uses an ordinary browser download. */
  let dlPromise = null;
  function hostDownloads() {
    if (!dlPromise) {
      const c = window.claude;
      dlPromise = c && typeof c.use === 'function' ? Promise.resolve(c.use('downloads')).catch(() => null) : Promise.resolve(null);
    }
    return dlPromise;
  }
  if (typeof window !== 'undefined' && window.claude) hostDownloads();
  function anchorDownload(filename, text) {
    try {
      const blob = new Blob([text], { type: 'text/csv;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = filename; a.rel = 'noopener';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 4000);
    } catch (e) { /* download blocked: the panel still has the data */ }
  }
  function exportCSV(filename, text, panel) {
    if (window.claude && typeof window.claude.use === 'function') {
      hostDownloads().then((dl) => {
        if (dl) return dl.save({ filename, data: text }).catch(() => { /* declined or unavailable: use the panel */ });
        anchorDownload(filename, text);
      });
    } else anchorDownload(filename, text);
    if (panel) {
      panel.hidden = false;
      panel.open = true;
      panel.querySelector('.fname').textContent = filename;
      panel.querySelector('textarea').value = text;
    }
  }
  function wireCopy(panel) {
    const btn = panel.querySelector('.copy');
    const ta = panel.querySelector('textarea');
    const msg = panel.querySelector('.copy-msg');
    btn.addEventListener('click', () => {
      const done = (t) => { msg.textContent = t; setTimeout(() => (msg.textContent = ''), 2500); };
      const fallback = () => { ta.focus(); ta.select(); done('Selected: press Ctrl/Cmd+C to copy'); };
      try {
        navigator.clipboard.writeText(ta.value).then(() => done('Copied'), fallback);
      } catch (e) { fallback(); }
    });
  }

  // ---------------------------------------------------------------- SVG plot
  const DASH = { theory: '', numeric: '7 4', measured: '', third: '7 3 1.5 3', fourth: '1.5 3', muted: '3 3', accent: '' };
  function niceStep(span, target) {
    const raw = span / Math.max(1, target);
    const p = Math.pow(10, Math.floor(Math.log10(raw)));
    const m = raw / p;
    return (m < 1.5 ? 1 : m < 3 ? 2 : m < 7 ? 5 : 10) * p;
  }
  function ticks(lo, hi, target) {
    const st = niceStep(hi - lo, target);
    const out = [];
    for (let t = Math.ceil(lo / st - 1e-9) * st; t <= hi + st * 1e-9; t += st) out.push(Math.abs(t) < st * 1e-9 ? 0 : t);
    return out;
  }
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  class Plot {
    /* opts: {xlabel, ylabel, aspect, logx, logy, xfmt, yfmt, legend: true} */
    constructor(container, opts = {}) {
      this.c = container;
      this.o = Object.assign({ aspect: 0.6, minH: 210, maxH: 430, xfmt: (v) => fmt(v, 3), yfmt: (v) => fmt(v, 3) }, opts);
      this.c.classList.add('plot');
      this.svgHolder = el('div');
      this.tip = el('div', { class: 'tip' }); this.tip.hidden = true;
      this.legendEl = el('div', { class: 'legend' });
      this.c.append(this.svgHolder, this.tip, this.legendEl);
      this.data = null;
      if (typeof ResizeObserver !== 'undefined') {
        let last = 0;
        new ResizeObserver(() => { const w = this.c.clientWidth; if (Math.abs(w - last) > 4 && this.data) { last = w; this.draw(this.data); } }).observe(this.c);
      }
      this.svgHolder.addEventListener('pointermove', (e) => this.hover(e));
      this.svgHolder.addEventListener('pointerleave', () => { this.tip.hidden = true; const d = this.svgHolder.querySelector('.hov'); if (d) d.setAttribute('visibility', 'hidden'); });
    }
    /* d: {series:[{x,y,role,label,width,markers,opacity,hover}], bands:[{x0,x1,label,labelPos:'top'|'bottom'}], points:[{x,y,role,shape,label,size}],
           segs:[{x0,y0,x1,y1,role,dash,width,label}], xlim, ylim, desc, texts:[{x,y,text,anchor,role,dx,dy (pixels)}]} */
    draw(d) {
      this.data = d;
      const o = this.o;
      const W = Math.max(280, this.c.clientWidth || 600);
      const H = Math.round(Math.min(o.maxH, Math.max(o.minH, W * o.aspect)));
      const m = { l: 58, r: 14, t: 12, b: 42 };
      const pw = W - m.l - m.r, ph = H - m.t - m.b;
      const tx = (v) => (o.logx ? Math.log10(v) : v), ty = (v) => (o.logy ? Math.log10(v) : v);
      let [x0, x1] = d.xlim, [y0, y1] = d.ylim;
      if (o.logx) { x0 = Math.log10(x0); x1 = Math.log10(x1); }
      if (o.logy) { y0 = Math.log10(y0); y1 = Math.log10(y1); }
      const sx = (v) => m.l + (tx(v) - x0) / (x1 - x0) * pw;
      const sy = (v) => m.t + ph - (ty(v) - y0) / (y1 - y0) * ph;
      this.map = { sx, sy, m, pw, ph };
      const id = 'c' + Math.random().toString(36).slice(2, 8);
      const parts = [];
      parts.push(`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${esc(d.desc || o.ylabel + ' versus ' + o.xlabel)}" xmlns="http://www.w3.org/2000/svg">`);
      parts.push(`<defs><clipPath id="${id}"><rect x="${m.l}" y="${m.t}" width="${pw}" height="${ph}"/></clipPath></defs>`);
      parts.push(`<rect x="${m.l}" y="${m.t}" width="${pw}" height="${ph}" style="fill:var(--panel)"/>`);
      // bands (regions where an assumption fails)
      for (const b of d.bands || []) {
        const a = Math.max(m.l, sx(b.x0)), z = Math.min(m.l + pw, sx(b.x1));
        if (z > a) {
          parts.push(`<rect x="${a}" y="${m.t}" width="${z - a}" height="${ph}" style="fill:var(--fail);opacity:.16"/>`);
          parts.push(`<line x1="${a}" y1="${m.t}" x2="${a}" y2="${m.t + ph}" style="stroke:var(--fail);stroke-width:1.2;stroke-dasharray:2 2"/>`);
          if (b.label) parts.push(`<text x="${a + 5}" y="${b.labelPos === 'bottom' ? m.t + ph - 6 : m.t + 13}" style="fill:var(--fail-ink);font-size:11px;font-weight:600">${esc(b.label)}</text>`);
        }
      }
      // grid + ticks
      const fs = 11;
      const xt = o.logx ? decades(d.xlim, Math.max(2, Math.floor(pw / 45))) : ticks(d.xlim[0], d.xlim[1], Math.max(3, Math.floor(pw / 85)));
      const yt = o.logy ? decades(d.ylim, Math.max(2, Math.floor(ph / 26))) : ticks(d.ylim[0], d.ylim[1], Math.max(3, Math.floor(ph / 45)));
      for (const t of xt) { const X = sx(o.logx ? 10 ** t : t); if (X < m.l - 0.5 || X > m.l + pw + 0.5) continue;
        parts.push(`<line x1="${X}" y1="${m.t}" x2="${X}" y2="${m.t + ph}" style="stroke:var(--grid);stroke-width:1"/>`);
        parts.push(`<line x1="${X}" y1="${m.t + ph}" x2="${X}" y2="${m.t + ph + 4}" style="stroke:var(--muted)"/>`);
        parts.push(`<text x="${X}" y="${m.t + ph + 16}" text-anchor="middle" style="fill:var(--muted);font-size:${fs}px" class="num">${esc(o.logx ? supExp(t) : o.xfmt(t))}</text>`); }
      for (const t of yt) { const Y = sy(o.logy ? 10 ** t : t); if (Y < m.t - 0.5 || Y > m.t + ph + 0.5) continue;
        parts.push(`<line x1="${m.l}" y1="${Y}" x2="${m.l + pw}" y2="${Y}" style="stroke:var(--grid);stroke-width:1"/>`);
        parts.push(`<line x1="${m.l - 4}" y1="${Y}" x2="${m.l}" y2="${Y}" style="stroke:var(--muted)"/>`);
        parts.push(`<text x="${m.l - 7}" y="${Y + 4}" text-anchor="end" style="fill:var(--muted);font-size:${fs}px" class="num">${esc(o.logy ? supExp(t) : o.yfmt(t))}</text>`); }
      parts.push(`<rect x="${m.l}" y="${m.t}" width="${pw}" height="${ph}" style="fill:none;stroke:var(--line)"/>`);
      parts.push(`<text x="${m.l + pw / 2}" y="${H - 6}" text-anchor="middle" style="fill:var(--ink);font-size:12px">${esc(o.xlabel)}</text>`);
      parts.push(`<text transform="translate(13 ${m.t + ph / 2}) rotate(-90)" text-anchor="middle" style="fill:var(--ink);font-size:12px">${esc(o.ylabel)}</text>`);
      parts.push(`<g clip-path="url(#${id})">`);
      // segments
      for (const s of d.segs || []) {
        parts.push(`<line x1="${sx(s.x0)}" y1="${sy(s.y0)}" x2="${sx(s.x1)}" y2="${sy(s.y1)}" style="stroke:var(--${s.role || 'mutedline'});stroke-width:${s.width || 1.2};stroke-dasharray:${s.dash || '4 3'};opacity:${s.opacity || 1}"/>`);
      }
      // series
      this.hoverPts = [];
      for (const s of d.series || []) {
        const n = Math.min(s.x.length, s.y.length);
        if (!n) continue;
        const col = `var(--${s.role || 'theory'})`;
        if (s.markers) {
          const stride = Math.max(1, Math.ceil(n / (s.maxMarkers || 350)));
          const r = s.r || 2.3;
          let g = '';
          for (let i = 0; i < n; i += stride) {
            const X = sx(s.x[i]), Y = sy(s.y[i]);
            if (!Number.isFinite(X) || !Number.isFinite(Y)) continue;
            g += `<circle cx="${X.toFixed(1)}" cy="${Y.toFixed(1)}" r="${r}"/>`;
            if (s.hover !== false) this.hoverPts.push([X, Y, s.x[i], s.y[i], s.label]);
          }
          parts.push(`<g style="fill:none;stroke:${col};stroke-width:1;opacity:${s.opacity || 0.85}">${g}</g>`);
        } else {
          let p = '', pen = false;
          for (let i = 0; i < n; i++) {
            const X = sx(s.x[i]), Y = sy(s.y[i]);
            if (!Number.isFinite(X) || !Number.isFinite(Y) || Math.abs(Y) > 1e5) { pen = false; continue; }
            p += (pen ? 'L' : 'M') + X.toFixed(1) + ' ' + Y.toFixed(1);
            pen = true;
            if (s.hover !== false && (i % Math.max(1, Math.floor(n / 400)) === 0 || i === n - 1)) this.hoverPts.push([X, Y, s.x[i], s.y[i], s.label]);
          }
          parts.push(`<path d="${p}" style="fill:none;stroke:${col};stroke-width:${s.width || 2};stroke-dasharray:${s.dash !== undefined ? s.dash : DASH[s.role] || ''};opacity:${s.opacity || 1};stroke-linejoin:round;stroke-linecap:round"/>`);
        }
      }
      parts.push('</g>');
      // points (markers with labels)
      for (const p of d.points || []) {
        const X = sx(p.x), Y = sy(p.y);
        if (!Number.isFinite(X) || !Number.isFinite(Y)) continue;
        const col = `var(--${p.role || 'ink'})`, z = p.size || 5;
        if (p.shape === 'diamond') parts.push(`<path d="M${X} ${Y - z - 1}L${X + z + 1} ${Y}L${X} ${Y + z + 1}L${X - z - 1} ${Y}Z" style="fill:var(--panel);stroke:${col};stroke-width:2"/>`);
        else if (p.shape === 'x') parts.push(`<path d="M${X - z} ${Y - z}L${X + z} ${Y + z}M${X - z} ${Y + z}L${X + z} ${Y - z}" style="stroke:${col};stroke-width:2.2"/>`);
        else if (p.shape === 'ring') parts.push(`<circle cx="${X}" cy="${Y}" r="${z + 2}" style="fill:none;stroke:${col};stroke-width:2.5"/><circle cx="${X}" cy="${Y}" r="2" style="fill:${col}"/>`);
        else parts.push(`<circle cx="${X}" cy="${Y}" r="${z}" style="fill:${p.fill ? col : 'var(--panel)'};stroke:${col};stroke-width:2"/>`);
        if (p.label) {
          const right = X < m.l + pw * 0.72;
          parts.push(`<text x="${X + (right ? 9 : -9)}" y="${Y - 8}" text-anchor="${right ? 'start' : 'end'}" style="fill:var(--ink);font-size:11px;font-weight:600;paint-order:stroke;stroke:var(--panel);stroke-width:3px">${esc(p.label)}</text>`);
        }
      }
      for (const t of d.texts || []) {
        parts.push(`<text x="${sx(t.x) + (t.dx || 0)}" y="${sy(t.y) + (t.dy || 0)}" text-anchor="${t.anchor || 'start'}" style="fill:var(--${t.role || 'muted'});font-size:11px;paint-order:stroke;stroke:var(--panel);stroke-width:3px">${esc(t.text)}</text>`);
      }
      parts.push(`<circle class="hov" r="4.5" visibility="hidden" style="fill:var(--accent);stroke:var(--panel);stroke-width:2"/>`);
      parts.push('</svg>');
      this.svgHolder.innerHTML = parts.join('');
      // legend
      if (this.o.legend !== false) {
        const items = (d.series || []).filter((s) => s.label && s.legend !== false).map((s) => {
          const col = `var(--${s.role || 'theory'})`;
          const sw = s.markers
            ? `<svg viewBox="0 0 26 10"><circle cx="13" cy="5" r="3" style="fill:none;stroke:${col};stroke-width:1.2"/></svg>`
            : `<svg viewBox="0 0 26 10"><line x1="1" y1="5" x2="25" y2="5" style="stroke:${col};stroke-width:2.2;stroke-dasharray:${s.dash !== undefined ? s.dash : DASH[s.role] || ''};opacity:${s.opacity || 1}"/></svg>`;
          return `<span>${sw}${esc(s.label)}</span>`;
        });
        for (const b of d.bands || []) if (b.legend) items.push(`<span><svg viewBox="0 0 26 10"><rect x="1" y="1" width="24" height="8" style="fill:var(--fail);opacity:.35"/></svg>${esc(b.legend)}</span>`);
        this.legendEl.innerHTML = items.join('');
      }
    }
    hover(e) {
      if (!this.hoverPts || !this.hoverPts.length) return;
      const svg = this.svgHolder.querySelector('svg');
      const r = svg.getBoundingClientRect();
      const k = svg.viewBox.baseVal.width / r.width;
      const X = (e.clientX - r.left) * k, Y = (e.clientY - r.top) * k;
      let best = null, bd = 1e9;
      for (const p of this.hoverPts) { const dd = (p[0] - X) ** 2 + (p[1] - Y) ** 2; if (dd < bd) { bd = dd; best = p; } }
      const dot = svg.querySelector('.hov');
      if (!best || bd > 900 * k * k) { this.tip.hidden = true; dot.setAttribute('visibility', 'hidden'); return; }
      dot.setAttribute('cx', best[0]); dot.setAttribute('cy', best[1]); dot.setAttribute('visibility', 'visible');
      this.tip.hidden = false;
      this.tip.textContent = `${best[4] ? best[4] + ': ' : ''}${this.o.xfmt(best[2])}, ${this.o.yfmt(best[3])}`;
      const left = best[0] / k + 12, top = best[1] / k - 30;
      this.tip.style.left = Math.min(left, r.width - this.tip.offsetWidth - 4) + 'px';
      this.tip.style.top = Math.max(0, top) + 'px';
    }
  }
  function decades(lim, maxN = 99) { const all = []; for (let e = Math.ceil(Math.log10(lim[0]) - 1e-9); e <= Math.floor(Math.log10(lim[1]) + 1e-9); e++) all.push(e); const step = Math.max(1, Math.ceil(all.length / maxN)); return all.filter((e) => e % step === 0); }
  function supExp(e) { if (e === 0) return '1'; if (e === 1) return '10'; return '10' + String(e).split('').map((c) => SUP[c] || c).join(''); }

  // least-squares slope of log(y) vs log(x)
  function logSlope(xs, ys) {
    const pts = xs.map((x, i) => [Math.log(x), Math.log(ys[i])]).filter((p) => Number.isFinite(p[0]) && Number.isFinite(p[1]));
    const n = pts.length; if (n < 2) return NaN;
    const mx = pts.reduce((a, p) => a + p[0], 0) / n, my = pts.reduce((a, p) => a + p[1], 0) / n;
    let sxy = 0, sxx = 0; for (const [a, b] of pts) { sxy += (a - mx) * (b - my); sxx += (a - mx) ** 2; }
    return sxy / sxx;
  }

  return { setSystem, onSystem, getSystem, conv, unconv, unit, csvUnit, fmt, fmtQ, plain, slider, segmented, toCSV, exportCSV, wireCopy, Plot, el, logSlope };
})();
