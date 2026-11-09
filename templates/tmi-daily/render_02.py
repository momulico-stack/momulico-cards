import sys,base64
sys.path.insert(0,'/home/claude/momulico-cards/tools')
import make_cards as mc
from playwright.sync_api import sync_playwright
from PIL import Image
def b(p): return "data:image/png;base64,"+base64.b64encode(open(p,'rb').read()).decode()
S={k:Image.open(k).size for k in ('st_b.png','st_a.png','st_c.png')}
html=f"""<!doctype html><html><head><meta charset="utf-8"><style>{mc.FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#000;font-family:'Pretendard'}}
.card{{position:relative;width:1080px;height:1350px;overflow:hidden;background:#000;color:#fff}}
.top{{position:absolute;z-index:5;top:64px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px}}
.top .rec{{width:12px;height:12px;border-radius:50%;background:{mc.GREEN}}}.top .logo{{font-size:26px;font-weight:600;letter-spacing:.08em;color:rgba(255,255,255,.9)}}
.n{{position:absolute;left:80px;top:420px;font-size:84px;font-weight:800;color:#fff;letter-spacing:-0.04em;line-height:1}}
.h{{position:absolute;left:80px;top:170px;font-size:84px;font-weight:800;letter-spacing:-0.04em;line-height:1.05}}
.h b{{background:{mc.GREEN};color:#fff;font-weight:800;padding:0 18px 6px;margin-left:4px}}
.p{{position:absolute;left:80px;width:760px;top:540px;font-size:31px;font-weight:500;line-height:1.6;text-align:justify;text-align-last:left;word-break:break-all;letter-spacing:-0.01em}}
.p::first-letter{{float:left;font-size:112px;line-height:.82;font-weight:800;margin:10px 14px 110px 0;color:#fff}}
.st{{position:absolute;z-index:4}}
</style></head><body><div class="card">
<div class="top"><span class="rec"></span><span class="logo">mmlc</span></div>
<div class="n">2.</div><div class="h">오늘의<br>영화 <b>TMI</b></div>
<p class="p">공포영화의 틀을 다진 앨프리드 히치콕은 무서워하는 것이 참 많았다. 그는 평생 경찰, 자동차, 그리고 달걀을 무서워했다.</p>
<img class="st" src="{b('st_a.png')}" style="left:90px;top:900px;width:{S['st_a.png'][0]}px">
<img class="st" src="{b('st_b.png')}" style="left:380px;top:800px;width:{S['st_b.png'][0]}px">
<img class="st" src="{b('st_c.png')}" style="left:770px;top:920px;width:{S['st_c.png'][0]}px">
</div></body></html>"""
with sync_playwright() as p:
    br=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]); pg=br.new_page(viewport={"width":1080,"height":1350})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path='card.png'); br.close()
Image.open('card.png').convert('RGB').save('card.jpg',quality=92)
