const fs = require('fs');
const vm = require('vm');
const path = require('path');
const source = fs.readFileSync(path.join(__dirname, '..', 'research-detail.html'), 'utf8');
function literalAfter(marker) {
  const start = source.indexOf(marker);
  if (start < 0) throw new Error('marker missing: ' + marker);
  const open = source.indexOf(marker.includes('[') ? '[' : '{', start);
  const closeFor = source[open] === '[' ? ']' : '}';
  let depth = 0, quote = null, escape = false;
  for (let i = open; i < source.length; i++) {
    const ch = source[i];
    if (quote) { if (escape) escape=false; else if (ch==='\\') escape=true; else if (ch===quote) quote=null; continue; }
    if (ch==='"' || ch==="'" || ch==='`') { quote=ch; continue; }
    if (ch===source[open]) depth++;
    if (ch===closeFor && --depth===0) return source.slice(open, i+1);
  }
  throw new Error('unclosed literal: ' + marker);
}
const studies = vm.runInNewContext('(' + literalAfter('var researchData = [') + ')');
const results = vm.runInNewContext('(' + literalAfter('var resultsBySlug = {') + ')');
const semantic = {
  'Objective':['Objective'], 'Hypothesis':['Hypothesis'], 'Methodology':['Methodology'],
  'Data Used':['Data Used','Data & Period','Data'], 'Results':['Results','Key Findings','Cycle Matrix'],
  'Charts':['Charts'], 'Conclusions':['Conclusions']
};
const keys=['sharpe','cagr','max_dd','win_rate','profit_factor','total_trades'];
const findings = studies.map(item => {
  const titles=(item.sections||[]).map(s=>s.title);
  const missing=Object.entries(semantic).filter(([,alts])=>!alts.some(x=>titles.includes(x))).map(([name])=>name);
  const empty=(item.sections||[]).filter(s=>!s.is_charts&&(!Array.isArray(s.content)||!s.content.join('').trim())).map(s=>s.title);
  const charts=(item.sections||[]).find(s=>s.title==='Charts');
  const r=results[item.slug];
  const metricIssue=!r || !r.ottimale || !r.realistico || ['ottimale','realistico'].some(mode=>keys.some(k=>typeof r[mode][k] !== 'number'));
  const badMode=r && keys.some(k=>r.realistico[k] > r.ottimale[k] && k !== 'max_dd');
  const placeholder=(JSON.stringify(item).match(/\bTODO\b|lorem ipsum|placeholder/ig)||[]).length;
  return {slug:item.slug,missing,empty,placeholder,metricIssue,badMode,chartSlug:charts&&charts.charts_slug,chartCount:charts&&charts.chart_descriptions&&charts.chart_descriptions.length};
});
const failures=findings.filter(x=>x.missing.length||x.empty.length||x.placeholder||x.metricIssue||x.badMode||!x.chartSlug||!x.chartCount);
console.log(JSON.stringify({studies:studies.length,resultSets:Object.keys(results).length,failures,findings},null,2));
if(studies.length!==13||Object.keys(results).length!==13||failures.length)process.exit(1);
