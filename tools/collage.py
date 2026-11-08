"""Collage helpers: grainy photo, torn-paper scrap around a cutout."""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np, cv2, random

W, H = 1080, 1350

def grain(im, sigma=16):
    arr = np.array(im.convert('RGBA')).astype(np.int16)
    n = np.random.normal(0, sigma, arr.shape[:2])
    for ch in range(3):
        arr[..., ch] = np.clip(arr[..., ch] + n, 0, 255)
    im = Image.fromarray(arr.astype(np.uint8), 'RGBA')
    im = ImageEnhance.Color(im).enhance(0.85)
    return ImageEnhance.Contrast(im).enhance(1.08)

def shadowed(im, tilt=0.0, blur=14, off=(10, 14), alpha=170):
    im = im.convert('RGBA')
    if tilt:
        im = im.rotate(tilt, resample=Image.BICUBIC, expand=True)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, alpha), (0, 0, im.width, im.height), im.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new('RGBA', (im.width + off[0] + blur, im.height + off[1] + blur), (0, 0, 0, 0))
    out.alpha_composite(sh, off)
    out.alpha_composite(im, (0, 0))
    return out

def photo(path, width, tilt=0.0):
    im = Image.open(path).convert('RGBA')
    im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    return shadowed(grain(im), tilt)

def scrap(cut_path, height, tilt=-2.5, margin=16, seed=3):
    random.seed(seed)
    cut = Image.open(cut_path).convert('RGBA')
    bb = cut.getbbox(); cut = cut.crop(bb)
    cut = cut.resize((int(cut.width * height / cut.height), height), Image.LANCZOS)
    cut = grain(cut, 18)
    pad = margin + 40
    CW, CH = cut.width + pad * 2, cut.height + pad * 2
    canvas = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); canvas.alpha_composite(cut, (pad, pad))
    alpha = np.array(canvas)[..., 3]
    mask = (alpha > 120).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    k = 2 * margin + 1
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(cnts, key=cv2.contourArea)
    approx = cv2.approxPolyDP(cnt, 6, True).reshape(-1, 2)
    pts = [(x + random.uniform(-6, 6), y + random.uniform(-6, 6)) for x, y in approx]
    paper = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    ImageDraw.Draw(paper).polygon(pts, fill=(245, 243, 238, 255))
    parr = np.array(paper).astype(np.int16); pn = np.random.normal(0, 6, parr.shape[:2])
    for ch in range(3):
        parr[..., ch] = np.clip(parr[..., ch] + pn, 0, 255)
    paper = Image.fromarray(parr.astype(np.uint8), 'RGBA')
    out = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); out.alpha_composite(paper); out.alpha_composite(cut, (pad, pad))
    out = out.crop(out.getbbox())
    return shadowed(out, tilt, blur=12, off=(8, 12))

def compose(items, out_path):
    """items: list of (PIL.Image RGBA, (x,y)) composited in order."""
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for im, pos in items:
        ov.alpha_composite(im, pos)
    ov.save(out_path)
    return ov
