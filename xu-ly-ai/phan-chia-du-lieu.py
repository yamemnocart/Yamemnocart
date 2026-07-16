import re
DAU_CAU = re.compile(r'[.!?]\s+')
def chia_thanh_doan_thong_minh(van_ban, toi_da=500):
    if not van_ban.strip(): return []
    if len(van_ban) <= toi_da: return [van_ban.strip()]
    cac_cau = DAU_CAU.split(van_ban)
    ket_qua=[]; hien_tai=""
    for c in cac_cau:
        c=c.strip()
        if not c: continue
        if len(hien_tai)+len(c)+1 <= toi_da:
            hien_tai = (hien_tai+" "+c).strip()
        else:
            if hien_tai: ket_qua.append(hien_tai)
            if len(c) > toi_da:
                # Cắt cứng nếu 1 câu quá dài
                for i in range(0,len(c),toi_da): ket_qua.append(c[i:i+toi_da])
                hien_tai=""
            else: hien_tai=c
    if hien_tai: ket_qua.append(hien_tai)
    return ket_qua
