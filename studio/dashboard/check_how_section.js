/* Checks the "Cómo funciona / Qué te llevas" block on the landing + orientation.
 * It went stale once already (described a course-shaped product months after the
 * goal engine shipped, and used retired "pregunta de defensa" wording), so the
 * promises are asserted here rather than trusted to review.
 *   node studio/dashboard/check_how_section.js
 */
const fs=require('fs'), vm=require('vm');
const html=fs.readFileSync('studio/dashboard/static/learn.html','utf8');
let src=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]).pop().replace(/\bboot\(\);\s*$/,'');
src=src.replace(/const \$=\(h\)=>\{[^\n]*\};/,'const $=(h)=>({__html:h,querySelector:()=>({onclick:null,style:{},value:"",classList:{add(){},remove(){},toggle(){}}}),querySelectorAll:()=>[],classList:{add(){},remove(){},toggle(){}},append(x){if(x&&x.__html)__cap.push(x.__html)},onclick:null,style:{},dataset:{},textContent:""});');
src=src.replace(/const app=document\.getElementById\('app'\), tabbar=document\.getElementById\('tabbar'\);/,'const app={innerHTML:"",append(x){if(x&&x.__html)__cap.push(x.__html)},querySelector:()=>({onclick:null}),querySelectorAll:()=>[]}; const tabbar={classList:{add(){},remove(){},toggle(){}}};');
const cap=[];
const sb={console,__cap:cap,document:{getElementById:()=>({}),createElement:()=>({}),addEventListener(){}},window:{addEventListener(){}},location:{hash:'',search:''},localStorage:{getItem:()=>null,setItem(){}},sessionStorage:{getItem:()=>null,setItem(){}},fetch:async()=>({ok:true,json:async()=>({})}),setTimeout:f=>{try{f()}catch(e){}},setInterval:()=>0,clearInterval(){},Date,Math,JSON,String,Number,Array,Object};
sb.globalThis=sb; vm.createContext(sb); vm.runInContext(src,sb);
vm.runInContext('renderHow(app)',sb);
const out=cap.join('\n');
const checks=[
 ['four numbered steps', ['1','2','3','4'].every(n=>out.includes(`>${n}</span>`))],
 ['step order: goal first', out.indexOf('Dinos qué quieres ser')<out.indexOf('Una lección al día')],
 ['project step present', out.includes('Elige tu proyecto real')],
 ['unlimited retries stated', out.includes('Reintentas sin límite')],
 ['AI-allowed stated', out.includes('Usar IA está permitido')],
 ['"Qué te llevas" section', out.includes('Qué te llevas')],
 ['deliverable promised', out.includes('El documento que vas a mostrar')],
 ['route visibility promised', out.includes('Tu ruta, siempre a la vista')],
 ['honest-gaps promised', out.includes('Lo que te falta, dicho por su nombre')],
 ['no-certificate line', out.includes('No damos certificados')],
 ['no stale "defensa" wording', !/pregunta de defensa/.test(out)],
 ['no stale "30 días"', !/30 d[ií]as/.test(out)],
 ['nothing undefined', !/\bundefined\b/.test(out)],
];
let bad=0; for(const [n,ok] of checks){ if(!ok)bad++; console.log((ok?'PASS  ':'FAIL  ')+n); }
console.log(`\n${checks.length-bad}/${checks.length} how-section checks passed`);
process.exit(bad?1:0);
