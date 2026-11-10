from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
def load(k,w=1400):
    im=Image.open(f'data/hi_{k}.jpg').convert('RGB')
    if im.width>w: im=im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
    return im
def grain(im,s=8):
    a=np.asarray(im).astype(float); a+=np.random.normal(0,s,a.shape[:2])[...,None]; return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def tint(im,rgb,amt):  # blend toward a color in shadows/mids
    a=np.asarray(im).astype(float); l=a.mean(2,keepdims=True)/255
    t=np.array(rgb)[None,None,:]; w=amt*(1-l)  # stronger in darks
    return Image.fromarray(np.clip(a*(1-w)+t*w,0,255).astype(np.uint8))
def split(im,sh,hi,amt):  # split tone
    a=np.asarray(im).astype(float); l=a.mean(2,keepdims=True)/255
    out=a+amt*((1-l)*(np.array(sh)-128)+l*(np.array(hi)-128))
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))
def duotone(im,dark,light):
    g=np.asarray(ImageOps.autocontrast(im.convert('L'),cutoff=1)).astype(float)/255
    out=np.array(dark)*(1-g[...,None])+np.array(light)*g[...,None]
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))
def cc(im,c=1,co=1,b=1):
    im=ImageEnhance.Color(im).enhance(c); im=ImageEnhance.Contrast(im).enhance(co); return ImageEnhance.Brightness(im).enhance(b)
def vignette(im,amt=0.35):
    w,h=im.size; y,x=np.mgrid[0:h,0:w]; r=np.sqrt(((x-w/2)/(w/2))**2+((y-h/2)/(h/2))**2)
    m=np.clip(1-amt*np.clip(r-0.5,0,1)/0.9,0,1); a=np.asarray(im).astype(float)*m[...,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def scan(im,period=4,amt=0.18):
    a=np.asarray(im).astype(float); m=np.ones(a.shape[0]); m[::period]=1-amt; return Image.fromarray(np.clip(a*m[:,None,None],0,255).astype(np.uint8))
def bloom(im,r=18,amt=0.35):
    bl=im.filter(ImageFilter.GaussianBlur(r)); a=np.asarray(im).astype(float); b=np.asarray(bl).astype(float)
    hi=np.clip((b-120)/135,0,1); return Image.fromarray(np.clip(a+amt*b*hi,0,255).astype(np.uint8))
def sepia(im,amt):
    g=ImageOps.colorize(im.convert('L'),(20,14,8),(255,238,210)); return Image.blend(im,g,amt)
G={
"br_user":    lambda im: grain(bloom(split(cc(im,1.35,1.12),(0,40,140),(255,90,210),0.5),20,0.6),4),  # 사이버펑크: 틸-마젠타 네온, 블룸
"348_mother": lambda im: grain(scan(split(cc(im,0.85,1.2,0.95),(30,50,20),(255,170,70),0.4),3,0.2),4),  # 카세트: 주황/앰버, 스캔라인, 거친 그레인
"19_b02":     lambda im: grain(vignette(sepia(cc(im,1,1.25),0.9),0.5),4),  # 레트로: 세피아 톤, 비네팅
"steam_user": lambda im: grain(vignette(split(cc(im,0.85,1.1),(60,40,60),(240,180,100),0.5),0.35),4),  # 스팀펑크: 황동/구리 웜톤
"island_user":lambda im: grain(duotone(cc(im,1,1.2),(2,10,16),(200,235,245)),4),  # 바이오펑크: 차가운 시안 듀오톤, 클리니컬
"180_b05":    lambda im: grain(cc(duotone(im,(4,8,20),(190,215,235)),1,1.1),4),  # 디스토피아: 탈색 스틸블루
"76341_b03":  lambda im: grain(split(cc(im,1.3,1.15),(10,40,120),(255,140,20),0.55),4),  # 포스트아포: 오렌지-틸 강하게
"clifi_user": lambda im: grain(tint(cc(im,0.45,1.15,1.05),(140,185,235),0.5),4),  # 클라이파이: 냉기, 채도 낮춤
"space_user": lambda im: grain(vignette(split(cc(im,1.1,1.25,0.92),(10,20,60),(255,200,150),0.3),0.6),4),  # 스페이스 오페라: 깊은 검정, 대비
}
if __name__=="__main__":
    import os; os.makedirs('graded',exist_ok=True)
    pairs=[]
    for k,f in G.items():
        im=load(k); out=f(im); out.save(f'graded/{k}.jpg',quality=93)
        a=im.resize((640,360)); b=out.resize((640,360)); pairs.append((a,b))
    sh=Image.new('RGB',(1280,(360+8)*len(pairs)),'black')
    for i,(a,b) in enumerate(pairs): sh.paste(a,(0,i*368)); sh.paste(b,(640,i*368))
    sh.save('grade_compare.jpg',quality=85)
