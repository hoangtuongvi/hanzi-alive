import {mkdir,writeFile} from 'node:fs/promises';
await mkdir('public/fonts',{recursive:true});
const url='https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;550;600;650;700&family=Libre+Caslon+Display&display=swap';
const res=await fetch(url,{headers:{'User-Agent':'Mozilla/5.0'}});if(!res.ok)throw Error('Font CSS failed');let css=await res.text();const urls=[...new Set([...css.matchAll(/url\((https:[^)]+)\)/g)].map(m=>m[1]))];
for(const [i,u] of urls.entries()){const r=await fetch(u);if(!r.ok)throw Error('Font file failed');const ext=u.includes('.woff2')?'woff2':'ttf';await writeFile(`public/fonts/font-${i}.${ext}`,new Uint8Array(await r.arrayBuffer()));css=css.replaceAll(u,`/fonts/font-${i}.${ext}`);}
await writeFile('public/fonts/fonts.css',css);
for(const [name,url] of [['DM-Sans-OFL.txt','https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/OFL.txt'],['Libre-Caslon-Display-OFL.txt','https://raw.githubusercontent.com/google/fonts/main/ofl/librecaslondisplay/OFL.txt']]){const r=await fetch(url);if(!r.ok)throw Error(`License ${r.status}`);await writeFile('public/licenses/'+name,await r.text());}
console.log('Cached font files:',urls.length);
