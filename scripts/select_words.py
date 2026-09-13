import json, pathlib, re
allwords=json.loads(pathlib.Path('data/source/complete-hsk-vocabulary-complete.json').read_text())
byword={x['simplified']:x for x in allwords}
stress='休 木 人 林 森 清 晴 请 情 青 河 可 月 肝 手 手掌 手机 高手 分手 对手 快乐 音乐 银行 行走 长大 长江 重要 重复 便宜 方便 东西 马虎 咖啡 葡萄 蝴蝶 巧克力 不好意思 莫名其妙 理所当然 自相矛盾 画蛇添足 一举两得 不知不觉'.split()
chars={x['character']:x for x in map(json.loads,pathlib.Path('data/source/makemeahanzi-dictionary.txt').read_text().splitlines())}
for w in stress:
 if w not in byword:
  ch=chars[w]; byword[w]={'simplified':w,'level':[],'pos':[],'forms':[{'traditional':w,'transcriptions':{'pinyin':ch['pinyin'][0]},'meanings':[ch.get('definition','')]}],'supplement':'Make Me a Hanzi'}
def level(x):return min([int(l[4:]) for l in x['level'] if re.fullmatch('old-[1-4]',l)] or [99])
pool=sorted([x for x in allwords if level(x)<99 and re.fullmatch('[\u3400-\u9fff]+',x['simplified'])],key=lambda x:(level(x),x.get('frequency',999999),x['simplified']))
selected=[byword[w] for w in stress];seen=set(stress)
for x in pool:
 if x['simplified'] not in seen:selected.append(x);seen.add(x['simplified'])
 if len(selected)==1000:break
pathlib.Path('data/selection.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
pathlib.Path('data/curation/stress.json').write_text(json.dumps(stress,ensure_ascii=False))
for start in range(0,1000,100):
 lines=[]
 for n,x in enumerate(selected[start:start+100],start+1):
  f=x['forms'][0]; lines.append(f"{n}. {x['simplified']} | {f['transcriptions']['pinyin']} | {'; '.join(f['meanings'][:3])}")
 pathlib.Path(f'data/curation/batch-{start//100+1:02d}-source.txt').write_text('\n'.join(lines))
print('selected',len(selected),'unique characters',len(set(''.join(x['simplified'] for x in selected))))
