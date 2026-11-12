import sys,base64
sys.path.insert(0,'/home/claude/momulico-cards/tools')
import make_cards as mc
from playwright.sync_api import sync_playwright
from PIL import Image
def b(p): return "data:image/png;base64,"+base64.b64encode(open(p,'rb').read()).decode()
S={k:Image.open(k).size for k in ('st_m3.png','st_g4.png','st_n04.png')}
html=f"""<!doctype html><html><head><meta charset="utf-8"><style>{mc.FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#000;font-family:'Pretendard'}}
.card{{position:relative;width:1080px;height:1350px;overflow:hidden;background:#000;color:#fff}}
.top{{position:absolute;z-index:5;top:64px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px}}
.top .rec{{width:12px;height:12px;border-radius:50%;background:{mc.GREEN}}}.top .logo{{font-size:26px;font-weight:600;letter-spacing:.08em;color:rgba(255,255,255,.9)}}
.n{{position:absolute;left:80px;top:420px;font-size:84px;font-weight:800;color:#fff;letter-spacing:-0.04em;line-height:1}}
.h{{position:absolute;left:80px;top:170px;font-size:84px;font-weight:800;letter-spacing:-0.04em;line-height:1.05}}
.h b{{background:{mc.GREEN};color:#fff;font-weight:800;padding:0 18px 6px;margin-left:4px}}
.p{{position:absolute;left:80px;width:860px;top:540px;text-align:left;font-size:31px;font-weight:500;line-height:1.6;text-align:justify;text-align-last:left;word-break:break-all;letter-spacing:-0.01em}}
.p::first-letter{{float:left;font-size:112px;line-height:.82;font-weight:800;margin:10px 14px 230px 0;color:#fff}}
.st{{position:absolute;z-index:4}}
</style></head><body><div class="card">
<div class="top"><span class="rec"></span><span class="logo">mmlc</span></div>
<div class="n">5.</div><div class="h">오늘의<br><b style="margin-left:0">TMI</b></div>
<p class="p">라이언 고슬링은 〈노트북〉 촬영 중 레이첼 맥아담스를 향해<br>“저 여자에게선 아무것도 느껴지지 않는다” 하여<br>대판 싸워놓고 촬영을 마치자마자 사귀었다.</p>
<img class="st" src="{b('st_m3.png')}" style="left:690px;top:110px;width:{S['st_m3.png'][0]}px">
<img class="st" src="{b('st_g4.png')}" style="left:70px;top:860px;width:{S['st_g4.png'][0]}px">
<img class="st" src="{b('st_n04.png')}" style="left:520px;top:800px;width:{S['st_n04.png'][0]}px">
</div></body></html>"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={"width":1080,"height":1350})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path='card.png'); br.close()
Image.open('card.png').convert('RGB').save('card.jpg',quality=92)
