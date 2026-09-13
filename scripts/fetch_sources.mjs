import {writeFile,mkdir} from 'node:fs/promises';
await mkdir('data/source',{recursive:true});
for (const repo of ['drkameleon/complete-hsk-vocabulary','skishore/makemeahanzi']) {
 const res=await fetch(`https://api.github.com/repos/${repo}/commits?per_page=1`); if(!res.ok) throw Error(`${res.status}`);
 const [{sha}]=await res.json(); console.log(repo,sha);
 const name=repo.split('/')[1];
 await writeFile(`data/source/${name}-revision.json`,JSON.stringify({repo,sha,url:`https://github.com/${repo}/tree/${sha}`},null,2));
 const paths=name.includes('hsk')?['complete.json','README.md','LICENSE']:['dictionary.txt','graphics.txt','COPYING','APL/english/ARPHICPL.TXT','LGPL'];
 await Promise.all(paths.map(async path=> { const r=await fetch(`https://raw.githubusercontent.com/${repo}/${sha}/${path}`); if(!r.ok)throw Error(`${path} ${r.status}`); const content=await r.text(); await writeFile(`data/source/${name}-${path.replaceAll('/','-')}`,content); console.log(path,content.length); }));
}
