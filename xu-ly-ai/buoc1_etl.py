import re, os, json, requests
from bs4 import BeautifulSoup
from underthesea import word_tokenize

REG_HTML = re.compile(r'<[^>]+>')
REG_DB   = re.compile(r'[^\w\s.?!,ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴÝỶỸ]')
REG_KT   = re.compile(r'\s+')

def lam_sach(text):
    text = REG_HTML.sub(' ', str(text))
    text = REG_DB.sub(' ', text)
    text = REG_KT.sub(' ', text).strip()
    return text.lower()

def tach_tu(text):
    if not text: return []
    return word_tokenize(text)

def khong_trung_lap(danh_sach_cau):
    dd=set(); kq=[]
    for c in danh_sach_cau:
        k=c[:60]
        if k not in dd: dd.add(k); kq.append(c)
    return kq

def luu_van_ban_goc(thu_muc, noi_dung, ten=None):
    import time
    ten = ten or f"vb_{int(time.time())}.txt"
    (thu_muc/ten).write_text(noi_dung,encoding="utf8")

def cao_web(url):
    try:
        r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"},timeout=15)
        r.encoding="utf8"
        return BeautifulSoup(r.text,"lxml").get_text("\n")
    except: return ""
