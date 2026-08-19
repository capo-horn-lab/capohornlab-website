const fs=require('fs'),vm=require('vm'),https=require('https'),path=require('path');
const s=fs.readFileSync(path.join(__dirname,'..','research-detail.html'),'utf8');
const marker='var researchData = [', start=s.indexOf(marker), open=s.indexOf('[',start);
let d=0,q=null,e=false,end=-1;
for(let i=open;i<s.length;i++){const c=s[i];if(q){if(e)e=false;else if(c==='\\')e=true;else if(c===q)q=null;continue}if(c==='"'||c==="'"||c==='`'){q=c;continue}if(c==='[')d++;if(c===']'&&--d===0){end=i+1;break}}
if(end<0)throw Error('unclosed researchData');
const studies=vm.runInNewContext('('+s.slice(open,end)+')');
const urls=[];
for(const study of studies){const sec=(study.sections||[]).find(x=>x.title==='Charts');for(const c of (sec&&sec.chart_descriptions)||[])urls.push({slug:study.slug,url:'https://www.capohornlab.com/research/charts/'+sec.charts_slug+'/'+c.id+'.png?v=godmodeqa20260819'});}
function get(item){return new Promise(resolve=>{const req=https.get(item.url,{headers:{'User-Agent':'CapoHornLab-QA/1.0'}},res=>{res.resume();resolve({...item,status:res.statusCode,bytes:Number(res.headers['content-length']||0)})});req.setTimeout(20000,()=>req.destroy(Error('timeout')));req.on('error',err=>resolve({...item,status:0,error:err.message}));});}
(async()=>{const all=[];for(const u of urls)all.push(await get(u));for(const item of all.filter(x=>x.status!==200)){const filename=item.url.split('/').pop().split('?')[0];const fallback=await get({...item,url:'https://www.capohornlab.com/research/charts/'+filename+'?v=godmodeqa20260819'});item.fallbackStatus=fallback.status;item.fallbackUrl=fallback.url;}const failed=all.filter(x=>x.status!==200&&x.fallbackStatus!==200);console.log(JSON.stringify({charts:all.length,primaryOk:all.filter(x=>x.status===200).length,renderable:all.length-failed.length,failed},null,2));if(failed.length)process.exit(1)})();
