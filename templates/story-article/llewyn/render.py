import sys,base64,io,os
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0,os.path.join(HERE,'../../../tools')); sys.path.insert(0,HERE)
import make_cards as mc
from grade import grain,cc
from playwright.sync_api import sync_playwright
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
W,H=1080,1350; G=mc.GREEN
def fit(im,w,h,fx=0.5,fy=0.5):
    s=max(w/im.width,h/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    x=int((im.width-w)*fx); y=int((im.height-h)*fy); return im.crop((x,y,x+w,y+h))
def b(im,q=90,fmt='JPEG'):
    bf=io.BytesIO(); im.save(bf,fmt,quality=q) if fmt=='JPEG' else im.save(bf,fmt); return f"data:image/{fmt.lower()};base64,"+base64.b64encode(bf.getvalue()).decode()
def tone(im): return grain(cc(im,0.9,1.05),5)
def bgdim(path,fx=0.5,fy=0.5,dark=0.28,blur=0):
    im=fit(Image.open(path).convert('RGB'),W,H,fx,fy)
    if blur: im=im.filter(ImageFilter.GaussianBlur(blur))
    a=np.asarray(ImageEnhance.Color(im).enhance(0.6)).astype(float)*dark
    return b(Image.fromarray(a.astype(np.uint8)))
def png(path,h):
    im=Image.open(path).convert('RGBA'); im=im.resize((int(im.width*h/im.height),h),Image.LANCZOS); return b(im,fmt='PNG'),im.width,im.height
CSS=f"""{mc.FONTS}*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#000;font-family:'Pretendard'}}
.card{{position:relative;width:1080px;height:1350px;overflow:hidden;background:#000;color:#fff}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.top{{position:absolute;z-index:9;top:64px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:10px}}
.top .rec{{width:12px;height:12px;border-radius:50%;background:{G}}}.top .logo{{font-size:26px;font-weight:600;letter-spacing:.08em;color:rgba(255,255,255,.9)}}
.cut{{position:absolute;z-index:3;filter:drop-shadow(0 24px 40px rgba(0,0,0,.8))}}
.bub{{position:absolute;z-index:5;background:#d9d9d9;color:#111;font-size:27px;font-weight:500;padding:18px 34px;border-radius:999px;white-space:nowrap;letter-spacing:-0.01em}}
.box{{position:absolute;z-index:6;left:70px;right:70px;background:rgba(236,236,236,.94);color:#111;font-size:28px;line-height:1.6;padding:26px 30px;word-break:keep-all;letter-spacing:-0.01em}}
.box b{{font-weight:800}}
.pl{{position:absolute;z-index:6;left:100px;right:100px;background:rgba(0,0,0,.82);color:#fff;border:1.5px solid rgba(255,255,255,.85);font-size:26px;line-height:1.55;padding:20px 26px;text-align:center;word-break:keep-all}}
.pl b{{font-weight:800}}
.cr{{position:absolute;left:0;right:0;bottom:36px;text-align:center;font-size:15px;color:rgba(255,255,255,.4);z-index:9}}
.sh{{position:absolute;left:0;right:0;bottom:0;height:700px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.92) 60%)}}
.h1{{position:absolute;z-index:6;left:72px;right:60px;bottom:120px;font-size:84px;font-weight:800;line-height:1.2;letter-spacing:-0.045em;word-break:keep-all}}
.h1 em{{font-style:normal;color:{G}}}
.pic{{position:absolute;background-size:cover;background-position:center}}
"""
TOP='<div class="top"><span class="rec"></span><span class="logo">mmlc</span></div>'
CR=''
def wrap(body,cover=False): return f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="card">{body}{TOP}{CR}</div></body></html>'
P=[]
# 1 cover
_pm=Image.open('post_main.jpg').convert('RGB'); _pm=_pm.crop((int(_pm.width*0.305),int(_pm.height*0.325),int(_pm.width*0.72),int(_pm.height*0.685)))
cov=tone(fit(_pm,W,H,0.5,0.5))
P.append(wrap(f'<div class="bg" style="background-image:url({b(cov)})"></div><div style="position:absolute;left:0;right:0;top:0;height:260px;background:linear-gradient(rgba(0,0,0,.75),rgba(0,0,0,0))"></div><div class="sh" style="height:800px"></div><div class="h1">코엔 형제가 그린<br>가장 아름다운 <em>미완</em></div>',cover=True))
# 2 origin — cat cutout
d,cw,ch=png('cut_cat.png',820)
P.append(wrap(f'''<div class="bg" style="background-image:url({bgdim('st6.jpg',0.5,0.5,0.22,6)})"></div>
<img class="cut" src="{d}" style="left:40px;top:170px;width:{cw}px">
<div class="box" style="top:880px;left:200px;right:70px">1961년 2월,<br>뉴욕 그리니치빌리지.<br>포크 가수 르윈 데이비스는 듀오 파트너를 잃고 혼자가 됐습니다.<br>앨범은 안 팔리고,<br>잠은 매일 남의 집 소파에서 자죠.<br>품에 안긴 고양이마저 <b>남의 집 고양이</b>입니다.</div>
'''))
# 3 real model — mic still full + sofa? use mic still as photo
mic=tone(fit(Image.open('st1.jpg').convert('RGB'),940,560,0.6,0.5))
P.append(wrap(f'''<div class="bg" style="background:#000"></div>
<div class="pic" style="left:70px;top:160px;width:940px;height:560px;background-image:url({b(mic)})"></div>
<div class="box" style="top:780px">르윈의 모델은 실존 포크 가수 <b>데이브 반 롱크</b>입니다.<br>코엔 형제는 그의 회고록 『맥두걸 스트리트의 시장』에서 이 영화를 출발시켰죠.<br>반 롱크는 무명이던 밥 딜런을 자기 집 소파에 재워 주던 선배였습니다.</div>
<div class="pl" style="top:1060px">딜런은 전설적인 포크 가수가 되었고,<br><b>반 롱크는 그 동네에 남았죠.</b></div>'''))
# 4 live recording — duet still + studio still
duet=tone(fit(Image.open('st3.jpg').convert('RGB'),940,400,0.5,0.45)); stu=tone(fit(Image.open('ex4.jpg').convert('RGB'),940,400,0.5,0.5))
P.append(wrap(f'''<div class="pic" style="left:70px;top:150px;width:940px;height:400px;background-image:url({b(duet)})"></div>
<div class="pic" style="left:70px;top:560px;width:940px;height:300px;background-image:url({b(stu)})"></div>
<div class="box" style="top:930px;font-size:26px">코엔 형제의 팬이던 오스카 아이작은 포크 영화 소식을 듣자마자 오디션에 매달렸습니다.<br>'Hang Me, Oh Hang Me'를 <b>4시간 동안 30번 넘게</b> 녹음해,<br>그중 하나를 골라 보냈죠.<br>준비하던 중엔 우연히 반 롱크와 함께 연주했던 기타리스트를 만나 직접 배우기도 했죠.</div>
'''))
# 5 cat Ulysses — cat cutout again, bigger, centered-right
d2,cw2,ch2=png('cut_cat.png',900)
P.append(wrap(f'''<div class="bg" style="background-image:url({bgdim('st2.jpg',0.2,0.5,0.2,8)})"></div>
<img class="cut" src="{d2}" style="left:40px;top:{1350-ch2-60}px;width:{cw2}px">
<div class="box" style="top:170px;left:420px;right:70px">르윈이 종일 안고 다니는 고양이의 이름은 <b>율리시스</b>.<br>『오디세이아』에서 10년을 떠돌다 집으로 돌아온 영웅의 이름이죠.</div>
'''))
# 6 awards — launch poster spotlight
_pl=Image.open('post_launch1.jpg').convert('RGB'); _pl=tone(_pl.resize((W,int(_pl.height*W/_pl.width)),Image.LANCZOS))
_top=tuple(int(v) for v in np.median(np.asarray(_pl.crop((0,0,300,30))).reshape(-1,3),0)); _band=grain(Image.new('RGB',(W,140),_top),5)
P.append(wrap(f'''<div class="bg" style="background:#000"></div><div class="pic" style="left:0;top:0;width:{W}px;height:140px;background-image:url({b(_band)})"></div><div class="pic" style="left:0;top:110px;width:{W}px;height:{_pl.height}px;background-image:url({b(_pl)})"></div><div class="sh" style="height:900px"></div>
<div class="box" style="top:720px">2013년 <b>칸영화제 심사위원대상</b>.<br>전미비평가협회 작품·감독·남우주연·촬영상 4관왕.<br>아카데미에선 촬영상과 음향상 후보에 올랐습니다.<br>통틀어 174개 부문 후보,<br>47개 수상이죠.</div>
'''))
# 7 why now — sofa cutout
d3,cw3,ch3=png('cut_sofa.png',720)
P.append(wrap(f'''<div class="bg" style="background-image:url({bgdim('st4.jpg',0.8,0.5,0.22,8)})"></div>
<img class="cut" src="{d3}" style="left:{1080-cw3-40}px;top:{1350-ch3-70}px;width:{cw3}px">
<div class="box" style="top:170px;left:70px;right:190px">국내에선 2014년 1월에 개봉했습니다.<br>그로부터 <b>12년</b>,<br>4K 리마스터링으로 다시 극장에 걸립니다.<br>브뤼노 델보넬이 찍은 잿빛 겨울과,<br>현장에서 라이브로 부른 노래를 큰 화면으로 다시 만날 기회죠.</div>
'''))
# 8 event
d4,cw4,ch4=png('cut_phone.png',620)
P.append(wrap(f'''<div class="bg" style="background:#000"></div>
<div style="position:absolute;left:72px;right:72px;top:170px;height:2px;background:{G}"></div>
<div style="position:absolute;left:80px;top:205px;font-size:24px;font-weight:600;color:{G};letter-spacing:.14em">EVENT</div>
<div style="position:absolute;left:80px;right:80px;top:250px;font-size:50px;font-weight:800;line-height:1.3;letter-spacing:-0.035em;word-break:keep-all">〈인사이드 르윈〉 기대평 댓글을 남겨주시면<br>추첨을 통해 <span style="color:{G}">예매권</span>을 드립니다!</div>
<img class="cut" src="{d4}" style="left:{1080-cw4-60}px;top:460px;width:{cw4}px;opacity:.95">
<div style="position:absolute;left:80px;top:470px;font-size:28px;line-height:2.0;font-weight:500"><b style="display:inline-block;width:150px;font-weight:700">응모 기간</b>11/17(화) ~ 11/23(월)<br><b style="display:inline-block;width:150px;font-weight:700">당첨 발표</b>11/30(월)<br><b style="display:inline-block;width:150px;font-weight:700">당첨 인원</b>10명 (1인 2매, 총 20매)<br><b style="display:inline-block;width:150px;font-weight:700">재개봉</b>12/2(수) · CGV 단독</div>
<div style="position:absolute;left:80px;right:80px;bottom:100px;font-size:19px;line-height:1.7;color:rgba(255,255,255,.55)">* 본 이벤트는 모물리코(@momulico.movie) 팔로워 대상 이벤트입니다.<br>* 비공개 계정은 당첨 안내 DM 발송이 어려워 선정에서 제외됩니다.<br>* 예매권은 당첨 발표일에 DM으로 발송됩니다.</div>
'''))
# 9 outro — launch poster 2 subway, no text
P.append(wrap(f'<div class="bg" style="background-image:url({b(tone(fit(Image.open("post_launch2.jpg").convert("RGB").crop((0,int(2400*0.12),1680,2400)),W,H,0.5,0.4)))})"></div>'))
os.makedirs('out',exist_ok=True)
with sync_playwright() as p:
    br=p.chromium.launch(**({"executable_path":"/usr/bin/google-chrome","args":["--no-sandbox"]} if os.path.exists("/usr/bin/google-chrome") else {})); pg=br.new_page(viewport={"width":W,"height":H})
    for i,h in enumerate(P,1):
        pg.set_content(h); pg.wait_for_timeout(300); pg.screenshot(path=f'out/card_{i}.png'); Image.open(f'out/card_{i}.png').convert('RGB').save(f'out/card_{i}.jpg',quality=92)
    br.close()
ims=[Image.open(f'out/card_{i}.jpg').resize((240,300)) for i in range(1,10)]
sh=Image.new('RGB',(240*9,300));[sh.paste(im,(i*240,0)) for i,im in enumerate(ims)];sh.save('contact.jpg',quality=88)
