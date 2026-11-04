#!/usr/bin/env python3
"""Verify only S07 differs from 0b10b63; exercise the original browser controls."""
import ast
import base64
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request

import websockets.sync.client

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DECK = ROOT / 'docs/defense/slide-deck-defense.html'
BUILDER = ROOT / 'docs/defense/build_defense_deck.py'
WORK = Path(os.environ.get('TMPDIR', str(Path.home()/'.cache'))) / 'defense-s7-verification'
WORK.mkdir(parents=True, exist_ok=True)


def git_bytes(path):
    return subprocess.check_output(['git','show',f'0b10b63:{path}'],cwd=ROOT)


class SlideSpans(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0]
        for m in re.finditer('\n', text): self.lines.append(m.end())
        self.depth = 0
        self.spans = []
        self.feed(text)

    def position(self):
        line, column = self.getpos()
        return self.lines[line-1]+column

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self.depth:
            self.depth += 1
        elif tag == 'div' and ('class','slide') in attrs:
            self.start = self.position()
            self.depth = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.depth:
            self.depth -= 1
            if not self.depth:
                self.spans.append((self.start,self.position()+len('</div>')))


before = git_bytes('docs/defense/slide-deck-defense.html').decode()
after = DECK.read_text()
a, b = SlideSpans(before).spans, SlideSpans(after).spans
assert len(a) == len(b) == 34
changed = [i+1 for i,(u,v) in enumerate(zip(a,b)) if before[slice(*u)] != after[slice(*v)]]
assert changed == [7], changed
assert before[:a[6][0]]+'<S07>'+before[a[6][1]:] == after[:b[6][0]]+'<S07>'+after[b[6][1]:]
old_ast = ast.parse(git_bytes('docs/defense/build_defense_deck.py').decode())
new_ast = ast.parse(BUILDER.read_text())
for tree in (old_ast,new_ast):
    tree.body = [n for n in tree.body if not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='S07' for t in n.targets))]
assert ast.dump(old_ast) == ast.dump(new_ast), 'Builder changed outside S07'
assert "User Progress (Future)" in after[slice(*b[6])]
assert "architecture-workflow-full.png" in BUILDER.read_text()
for i,script in enumerate(re.findall(r'<script>(.*?)</script>',after,re.S)):
    p = WORK / f'inline-{i}.js'
    p.write_text(script)
    subprocess.run(['node','--check',str(p)],check=True)

# Pin untouched variant files against the pre-edit manifest when available.
manifest = HERE/'initial-hashes.json'
untouched = {}
if manifest.exists():
    hashes = json.loads(manifest.read_text())
    for name in ('build_defense_deck_v2.py','slide-deck-defense-v2.html',
                 'build_defense_deck_focus.py','slide-deck-defense-focus.html'):
        untouched[name] = hashlib.sha256((ROOT/'docs/defense'/name).read_bytes()).hexdigest() == hashes[name]
    assert all(untouched.values()), untouched

baseline_file = WORK/'baseline.html'
baseline_file.write_text(before)
short = Path.home()/'.cache/defense-s7-tmp'
if not short.exists(): short.symlink_to(WORK,target_is_directory=True)
assert short.is_symlink() and short.resolve() == WORK.resolve()
profile = WORK/'chrome-profile'
portfile = profile/'DevToolsActivePort'
portfile.unlink(missing_ok=True)
env = os.environ.copy()
env['TMPDIR'] = str(short)
log = (WORK/'chromium.log').open('w')
proc = subprocess.Popen(['/usr/sbin/chromium','--headless=new','--disable-gpu',
    '--remote-debugging-port=0','--user-data-dir='+str(profile),
    '--no-first-run','--no-default-browser-check'],env=env,stdout=log,stderr=log)
try:
    for _ in range(100):
        if portfile.exists(): break
        assert proc.poll() is None, 'Chromium exited; inspect '+str(WORK/'chromium.log')
        time.sleep(.1)
    port = int(portfile.read_text().splitlines()[0])
    req = urllib.request.Request(f'http://127.0.0.1:{port}/json/new?about:blank',method='PUT')
    tab = json.load(urllib.request.urlopen(req))
    with websockets.sync.client.connect(tab['webSocketDebuggerUrl'],max_size=100_000_000) as ws:
        ident = 0
        exceptions = []
        def call(method, **params):
            global ident
            ident += 1
            ws.send(json.dumps({'id':ident,'method':method,'params':params}))
            while True:
                message = json.loads(ws.recv())
                if message.get('method') == 'Runtime.exceptionThrown': exceptions.append(message)
                if message.get('id') == ident:
                    assert 'error' not in message, message
                    return message.get('result',{})
        def ev(expression):
            result = call('Runtime.evaluate',expression=expression,returnByValue=True,awaitPromise=True)
            assert 'exceptionDetails' not in result,result
            return result['result'].get('value')
        def key(value, code=None):
            call('Input.dispatchKeyEvent',type='keyDown',key=value,code=code or value)
            call('Input.dispatchKeyEvent',type='keyUp',key=value,code=code or value)
        def click(selector):
            pos = ev('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2};})()')
            call('Input.dispatchMouseEvent',type='mousePressed',button='left',clickCount=1,**pos)
            call('Input.dispatchMouseEvent',type='mouseReleased',button='left',clickCount=1,**pos)
        def load(path):
            call('Page.navigate',url=path.as_uri())
            for _ in range(300):
                if ev("document.readyState==='complete' && typeof goToSlide==='function' && !!document.querySelector('.katex')"): break
                time.sleep(.1)
            assert ev("typeof goToSlide==='function' && !!document.querySelector('.katex')"), 'Navigation or KaTeX did not load'
            ev('document.fonts.ready.then(()=>true)')
        def formula_inventory():
            return ev("Array.from(document.querySelectorAll('.deck-canvas>.slide')).map(s=>({math:s.querySelectorAll('.katex').length,errors:s.querySelectorAll('.katex-error').length,formulas:Array.from(s.querySelectorAll('annotation[encoding=\"application/x-tex\"]')).map(n=>n.textContent)}))")
        call('Runtime.enable'); call('Page.enable')
        call('Emulation.setDeviceMetricsOverride',width=1280,height=800,deviceScaleFactor=1,mobile=False)
        load(baseline_file)
        baseline_math = formula_inventory()
        load(DECK)
        final_math = formula_inventory()
        assert baseline_math == final_math, 'Math changed'
        assert len(final_math)==34 and all(m['errors']==0 for m in final_math)
        assert sum(m['math'] for m in final_math)>0
        assert ev("getComputedStyle(document.querySelector('.top-nav')).display!=='none' && getComputedStyle(document.querySelector('.bottom-footer')).display!=='none'")
        assert not ev("!!document.getElementById('chromeToggle')"), 'Unexpected focus control'
        ev('goToSlide(6)')
        key('ArrowRight'); assert ev('currentSlide')==7
        key('ArrowLeft'); assert ev('currentSlide')==6
        key('g','KeyG'); assert ev("document.getElementById('modalOverlay').classList.contains('active')")
        key('Escape'); assert not ev("document.getElementById('modalOverlay').classList.contains('active')")
        screenshots, geometry = [], []
        for width,height in ((1280,800),(1920,1080)):
            call('Emulation.setDeviceMetricsOverride',width=width,height=height,deviceScaleFactor=1,mobile=False)
            ev('goToSlide(6)'); time.sleep(.35)
            r = ev("(()=>{const s=slides[6],r=s.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,scrollWidth:s.scrollWidth,clientWidth:s.clientWidth,scrollHeight:s.scrollHeight,clientHeight:s.clientHeight,innerOverflow:Array.from(s.querySelectorAll('.academic-card')).map(e=>({x:e.scrollWidth-e.clientWidth,y:e.scrollHeight-e.clientHeight}))};})()")
            assert r['scrollWidth']<=r['clientWidth']+1 and r['scrollHeight']<=r['clientHeight']+1,r
            assert all(c['x']<=1 and c['y']<=1 for c in r['innerOverflow']),r
            assert r['x']>=-1 and r['y']>=-1 and r['x']+r['width']<=width+1 and r['y']+r['height']<=height+1,r
            geometry.append(dict(viewport=[width,height],**r))
            shot = HERE/f'slide-07-{width}x{height}.png'
            shot.write_bytes(base64.b64decode(call('Page.captureScreenshot',format='png')['data']))
            screenshots.append(shot.name)
        click('.deck-canvas>.slide:nth-child(7) button[aria-label]')
        assert ev("getComputedStyle(document.getElementById('imageLightboxModal')).display==='flex'")
        assert ev("document.getElementById('lightboxImg').naturalWidth>0")
        key('Escape'); assert ev("getComputedStyle(document.getElementById('imageLightboxModal')).display==='none'")
        for i in range(34): ev(f'goToSlide({i})'); assert ev('currentSlide')==i
        broken = ev("Array.from(document.querySelectorAll('.deck-canvas img')).filter(i=>!i.complete||!i.naturalWidth).length")
        assert broken==0 and not exceptions,(broken,exceptions)
        report = {'slide_count':34,'changed_slides':changed,'other_slides_byte_exact':True,
                  'outside_s07_byte_exact':True,'builder_only_s07_changed':True,
                  'baseline_commit':'0b10b63','deck_sha256':hashlib.sha256(DECK.read_bytes()).hexdigest(),
                  'variant_files_unchanged':untouched,'math_count':sum(m['math'] for m in final_math),
                  'math_formula_inventory_unchanged':True,'katex_errors':0,'broken_images':broken,
                  'javascript_exceptions':exceptions,'javascript_syntax':'pass',
                  'keyboard_navigation_overview_lightbox':'pass','geometry':geometry,'screenshots':screenshots}
        (HERE/'deck-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='geometry'},ensure_ascii=False,indent=2))
finally:
    proc.terminate()
    proc.wait(timeout=10)
    log.close()
