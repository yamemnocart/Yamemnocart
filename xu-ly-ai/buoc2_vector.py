from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

mo_hinh = None
kich_thuoc_vector = 100

def tao_vector(danh_sach_tu):
    global mo_hinh
    if len(danh_sach_tu) < 2:
        return []
    # Huấn luyện mô hình nếu chưa có
    if mo_hinh is None:
        mo_hinh = Word2Vec([danh_sach_tu], vector_size=kich_thuoc_vector, window=5, min_count=1, workers=2)
    else:
        mo_hinh.build_vocab([danh_sach_tu], update=True)
        mo_hinh.train([danh_sach_tu], total_examples=1, epochs=5)
    # Chuyển thành vector
    vector_tong = np.zeros(kich_thuoc_vector)
    so_tu = 0
    for tu in danh_sach_tu:
        if tu in mo_hinh.wv:
            vector_tong += mo_hinh.wv[tu]
            so_tu += 1
    return vector_tong / so_tu if so_tu > 0 else []

def tim_tuong_thich(vector_cau_hoi, danh_sach_vector, danh_sach_van_ban, so_luong=5):
    if not danh_sach_vector or len(vector_cau_hoi) == 0:
        return []
    # Tìm độ tương đồng cosine
    do_tuong_thich = [cosine_similarity([vector_cau_hoi], [vec])[0][0] for vec in danh_sach_vector]
    chi_so_sap_xep = np.argsort(do_tuong_thich)[-so_luong:][::-1]
    return [danh_sach_van_ban[i] for i in chi_so_sap_xep if do_tuong_thich[i] > 0.3]
