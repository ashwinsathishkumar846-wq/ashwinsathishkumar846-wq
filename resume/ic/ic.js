const {chromium}=require('playwright'),fs=require('fs');
const gh=fs.readFileSync('node_modules/simple-icons/icons/github.svg','utf8').match(/d="([^"]+)"/)[1];
const lc=fs.readFileSync('node_modules/simple-icons/icons/leetcode.svg','utf8').match(/d="([^"]+)"/)[1];
const S={
mail:`<svg viewBox="0 0 24 24" fill="none" stroke="#222" stroke-width="1.6" stroke-linejoin="round"><rect x="2.5" y="5" width="19" height="14" rx="1.5"/><path d="M3 6.5l9 7 9-7"/></svg>`,
phone:`<svg viewBox="0 0 24 24" fill="#111"><path d="M6.6 10.8a15 15 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z"/></svg>`,
in:`<svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="3" fill="#111"/><rect x="5.2" y="9.5" width="2.8" height="8.8" fill="#fff"/><circle cx="6.6" cy="6.4" r="1.7" fill="#fff"/><path d="M10.2 9.5h2.7v1.3c.6-1 1.6-1.5 2.9-1.5 2.4 0 3 1.6 3 3.7v5.3h-2.8v-4.7c0-1.1-.2-1.9-1.3-1.9s-1.7.8-1.7 2v4.6h-2.8z" fill="#fff"/></svg>`,
gh:`<svg viewBox="0 0 24 24" fill="#111"><path d="${gh}"/></svg>`,
lc:`<svg viewBox="0 0 24 24" fill="#111"><path d="${lc}"/></svg>`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:96,height:96},deviceScaleFactor:3});
for(const k in S){await p.setContent(`<body style="margin:0;background:transparent"><div style="width:96px;height:96px;padding:10px 8px 0 8px">${S[k].replace("<svg","<svg width=\"80\" height=\"80\"")}</div></body>`);await p.screenshot({path:`../icon_${k}.png`,omitBackground:true});}
await b.close()})();
