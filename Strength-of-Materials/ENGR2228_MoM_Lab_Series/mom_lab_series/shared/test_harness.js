/* Load the exact <script id="model"> block a simulation page runs, for Node tests. */
'use strict';
const fs = require('fs');
const vm = require('vm');

function loadModel(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const m = html.match(/<script id="model">([\s\S]*?)<\/script>/);
  if (!m) throw new Error('no <script id="model"> block in ' + htmlPath);
  const ctx = { module: { exports: {} }, Math, console };
  vm.createContext(ctx);
  vm.runInContext(m[1], ctx, { filename: htmlPath + '#model' });
  return ctx.module.exports;
}

/* Load the shared SimCore (units, formatting) exactly as inlined in the page. */
function loadSimCore(htmlPath) {
  const html = fs.readFileSync(htmlPath, 'utf8');
  const a = html.indexOf('const SimCore = (() =>');
  const b = html.indexOf('})();', html.indexOf('return { setSystem', a)) + 5;
  const ctx = { Math, Number, String, console };
  vm.createContext(ctx);
  vm.runInContext(html.slice(a, b) + '\nglobalThis.SimCore = SimCore;', ctx);
  return ctx.SimCore;
}

const results = [];
function check(name, measured, expected, tol, note = '') {
  const rel = Math.abs(measured - expected) / Math.max(Math.abs(expected), 1e-300);
  const pass = rel <= tol;
  results.push({ name, measured, expected, rel, tol, pass, note });
  return pass;
}
function checkAbs(name, measured, expected, tol, note = '') {
  const d = Math.abs(measured - expected);
  const pass = d <= tol;
  results.push({ name: name + ' (absolute difference)', measured, expected, rel: d, tol, pass, note });
  return pass;
}
function checkTrue(name, cond, note = '') { results.push({ name, measured: cond, expected: true, rel: cond ? 0 : 1, tol: 0, pass: !!cond, note }); return cond; }
function report(title) {
  const lines = [`## ${title}`, '', '| Test | Value | Reference | Rel. difference | Tolerance | Result |', '|---|---:|---:|---:|---:|---|'];
  for (const r of results) {
    const f = (v) => (typeof v === 'boolean' ? String(v) : Number(v).toPrecision(8));
    lines.push(`| ${String(r.name + (r.note ? ' — ' + r.note : '')).replace(/\|/g, '\\|')} | ${f(r.measured)} | ${f(r.expected)} | ${r.rel.toExponential(2)} | ${r.tol.toExponential(1)} | ${r.pass ? 'PASS' : '**FAIL**'} |`);
  }
  const nfail = results.filter((r) => !r.pass).length;
  lines.push('', `${results.length - nfail} of ${results.length} passed.`);
  return { text: lines.join('\n'), nfail };
}
module.exports = { loadModel, loadSimCore, check, checkAbs, checkTrue, report, results };
