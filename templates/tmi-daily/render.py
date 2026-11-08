import sys,base64
sys.path.insert(0,'/home/claude/momulico-cards/tools')
import make_cards as mc
from playwright.sync_api import sync_playwright
from PIL import Image
def b(p): return "data:image/png;base64,"+base64.b64encode(open(p,'rb').read()).decode()
S={k:Image.open(k).size for k in ('st_cut_s.png','st_cut_fight.png','st_cut_back.png')}
html=f"""<!doctype html><html><head><meta charset="utf-8"><style>{mc.FONTS}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#000;font-family:'Pretendard'}}
.card{{position:relative;width:1080px;height:1350px;overflow:hidden;background:#000;color:#fff}}
.top{{position:absolute;z-index:5;top:64px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px}}
.top .rec{{width:12px;height:12px;border-radius:50%;background:{mc.GREEN}}}.top .logo{{font-size:26px;font-weight:600;letter-spacing:.08em;color:rgba(255,255,255,.9)}}
.n{{position:absolute;left:80px;top:500px;font-size:84px;font-weight:800;color:#fff;letter-spacing:-0.04em;line-height:1}}
.h{{position:absolute;left:80px;top:170px;font-size:84px;font-weight:800;letter-spacing:-0.04em;line-height:1.05}}
.h b{{background:{mc.GREEN};color:#fff;font-weight:800;padding:0 18px 6px;margin-left:4px}}
.p{{position:absolute;left:80px;width:640px;top:640px;font-size:31px;font-weight:500;line-height:1.6;text-align:justify;text-align-last:justify;word-break:break-all;letter-spacing:-0.01em}}
.p::first-letter{{float:left;font-size:112px;line-height:.82;font-weight:800;margin:10px 14px 110px 0;color:#fff}}
.st{{position:absolute;z-index:4}}
</style></head><body><div class="card">
<div class="top"><span class="rec"></span><span class="logo">mmlc</span></div>
<div class="n">1.</div><div class="h">오늘의<br>영화 <b>TMI</b></div>
<p class="p">이소룡은 1958년 홍콩 차차차 댄스 챔피언 출신입니다. 미국으로 건너갈 때조차 차차차의 <nobr>108가지</nobr> 스텝을 꼼꼼히 적은 노트를<br><span style="display:inline-block;text-align:left">챙겨 갔다고 합니다.</span></p>
<img class="st" src="{b('st_cut_fight.png')}" style="left:660px;top:230px;width:{S['st_cut_fight.png'][0]}px">
<img class="st" src="{b('st_cut_s.png')}" style="left:790px;top:640px;width:{S['st_cut_s.png'][0]}px">
<img class="st" src="{b('st_cut_back.png')}" style="left:140px;top:930px;width:{S['st_cut_back.png'][0]}px">
</div></body></html>"""
with sync_playwright() as p:
    br=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"]); pg=br.new_page(viewport={"width":1080,"height":1350})
    pg.set_content(html); pg.wait_for_timeout(300); pg.screenshot(path='v3.png'); br.close()
Image.open('v3.png').convert('RGB').save('v3.jpg',quality=92)
