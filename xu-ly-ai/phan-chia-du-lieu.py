def chia_nho_van_ban(noi_dung, do_dai_toi_da=500):
    # Chia theo dấu câu để không cắt giữa câu
    cac_doan = []
    bat_dau = 0
    while bat_dau < len(noi_dung):
        ket_thuc = bat_dau + do_dai_toi_da
        if ket_thuc >= len(noi_dung):
            cac_doan.append(noi_dung[bat_dau:].strip())
            break
        # Tìm vị trí dấu câu gần nhất
        vi_tri_dau = max(
            noi_dung.rfind('. ', bat_dau, ket_thuc),
            noi_dung.rfind('! ', bat_dau, ket_thuc),
            noi_dung.rfind('? ', bat_dau, ket_thuc)
        )
        ket_thuc = vi_tri_dau + 2 if vi_tri_dau > bat_dau else ket_thuc
        cac_doan.append(noi_dung[bat_dau:ket_thuc].strip())
        bat_dau = ket_thuc
    return [doan for doan in cac_doan if doan]
