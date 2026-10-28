"""Validate source coverage, citations, routes, and local media."""
from pathlib import Path
import json,re
from html.parser import HTMLParser

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/content.json').read_text())
assert (root/'data/content.js').read_text().startswith('window.CUPS = ')
js=(root/'data/content.js').read_text()[len('window.CUPS = '):].rstrip().removesuffix(';').replace('<\\/','</')
assert json.loads(js)==data
messages=[m for s in data['sources'] for c in s['channels'] for m in c['messages']]
ids={m['id'] for m in messages}
assert len(ids)==len(messages)==data['stats']['messages']==119
assert len({s['id'] for s in data['sources']})==2
assert sum(len(s['channels']) for s in data['sources'])==33
article_ids={a['id'] for a in data['articles']}
issue_ids={i['id'] for i in data['issues']}
assert len(article_ids)==len(data['articles'])==22
assert len(issue_ids)==len(data['issues'])==29
for i in data['issues']:
    assert all(mid in ids for mid in i['refs']),i['id']
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        attr=dict(attrs); href=attr.get('href','')
        if href.startswith('#sources/message/'):assert href.split('/')[-1] in ids,href
        if href.startswith('#problems/'):assert href.split('/')[-1] in issue_ids,href
for a in data['articles']:Links().feed(a['body'])
media=[]
for s in data['sources']:
    for c in s['channels']:
        for m in c['messages']:
            assert m['url']==f'https://discord.com/channels/{s["id"]}/{c["id"]}/{m["id"]}'
            for a in m['attachments']:
                if data.get('imagesPublished'):
                    assert a['path'] and (root/a['path']).is_file(),a
                else:
                    assert a['path'] is None,a
                media.append(a)
assert len(media)==81
assert sum(bool(a['map']) for a in media)==7
assert len(data['sources'][1]['issues'])==9
for source in data['sources']:
    assert not any('Authorization' in m['content'] for c in source['channels'] for m in c['messages'] if m['content'])
print('PASS: 119 messages, 33 channels, 22 articles, 29 issues, 81 attachment references, 7 maps; all citations and routes resolve')
