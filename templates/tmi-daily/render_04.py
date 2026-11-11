import sys,base64
sys.path.insert(0,'/home/claude/momulico-cards/tools')
import make_cards as mc
from playwright.sync_api import sync_playwright
from PIL import Image
def b(p): return "data:image/png;base64,"+base64.b64encode(open(p,'rb').read()).decode()
S={k:Image.open(k).size for k in ('st_young.png','st_old.png','st_dooku.png','st_saru.png')}
html=f"""<!doctype html><html><head><meta charset="utf-8"><style>{mc.FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#000;font-family:'Pretendard'}}
.card{{position:relative;width:1080px;height:1350px;overflow:hidden;background:#000;color:#fff}}
.top{{position:absolute;z-index:5;top:64px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px}}
.top .rec{{width:12px;height:12px;border-radius:50%;background:{mc.GREEN}}}.top .logo{{font-size:26px;font-weight:600;letter-spacing:.08em;color:rgba(255,255,255,.9)}}
.n{{position:absolute;left:80px;top:420px;font-size:84px;font-weight:800;color:#fff;letter-spacing:-0.04em;line-height:1}}
.h{{position:absolute;left:80px;top:170px;font-size:84px;font-weight:800;letter-spacing:-0.04em;line-height:1.05}}
.h b{{background:{mc.GREEN};color:#fff;font-weight:800;padding:0 18px 6px;margin-left:4px}}
.p{{position:absolute;left:80px;width:720px;top:540px;font-size:31px;font-weight:500;line-height:1.6;text-align:justify;text-align-last:left;word-break:break-all;letter-spacing:-0.01em}}
.p::first-letter{{float:left;font-size:112px;line-height:.82;font-weight:800;margin:10px 14px 230px 0;color:#fff}}
.st{{position:absolute;z-index:4}}
</style></head><body><div class="card">
<div class="top"><span class="rec"></span><span class="logo">mmlc</span></div>
<div class="n">4.</div><div class="h">오늘의<br><b style="margin-left:0">TMI</b></div>
<p class="p">크리스토퍼 리는 〈반지의 제왕〉 배우 중 유일하게 톨킨을 직접 만난 사람이다. 옥스퍼드의 한 펍에서 우연히 마주친 그는 소녀팬같이 기어들어가는 설레는 목소리로 “안녕하십니까” 한마디밖에 못 했다고 한다. 그럼에도 그에겐 평생 꿈꾸던 간달프 역할이 아닌, 사루만 역이 주어졌다.</p>
<img class="st" src="{b('st_young.png')}" style="left:690px;top:120px;width:{S['st_young.png'][0]}px">
<img class="st" src="{b('st_old.png')}" style="left:50px;top:940px;width:{S['st_old.png'][0]}px">
<img class="st" src="{b('st_dooku.png')}" style="left:400px;top:920px;width:{S['st_dooku.png'][0]}px">
<img class="st" src="{b('st_saru.png')}" style="left:770px;top:850px;width:{S['st_saru.png'][0]}px">
</div></body></html>"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={"width":1080,"height":1350})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path='card.png'); br.close()
Image.open('card.png').convert('RGB').save('card.jpg',quality=92)
