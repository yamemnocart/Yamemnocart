import os, json, numpy as np
from gensim.models import Word2Vec
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity

class Word2VecAI:
    def __init__(self, thu_muc_luu, kich=128):
        self.tm=thu_muc_luu; self.k=kich
        self.dh = thu_muc_luu/"w2v.model"
        self.dong_xuat = defaultdict(int)
        self.kho_ngu_canh = []
        self._tai()
    def _tai(self):
        if self.dh.exists():
            self.m = Word2Vec.load(str(self.dh))
        else:
            self.m = None
        if (self.tm/"ngu_canh.json").exists():
            self.kho_ngu_canh = json.loads((self.tm/"ngu_canh.json").read_text(encoding="utf8"))
    def _luu(self):
        if self.m: self.m.save(str(self.dh))
        (self.tm/"ngu_canh.json").write_text(json.dumps(self.kho_ngu_canh,ensure_ascii=False),encoding="utf8")
    def huan_luyen(self, mang_cau):
        if not mang_cau: return
        # XÂY DỰNG MA TRẬN ĐỒNG XUẤT HIỆN
        for cau in mang_cau:
            for i,t in enumerate(cau):
                for j in range(max(0,i-3),min(len(cau),i+4)):
                    if i!=j: self.dong_xuat[(t,cau[j])]+=1
        if self.m is None:
            self.m = Word2Vec(mang_cau,vector_size=self.k,window=4,min_count=1,workers=2,sg=1)
        else:
            self.m.build_vocab(mang_cau, update=True)
            self.m.train(mang_cau, total_examples=len(mang_cau), epochs=6)
        # Lưu vector ngữ cảnh
        for cau in mang_cau:
            v = self.vector_cau(cau)
            if v is not None:
                self.kho_ngu_canh.append({"tu":cau,"vec":v.tolist()})
        self._luu()
    def vector_cau(self, tu_danh_sach):
        if not self.m: return None
        ds=[self.m.wv[t] for t in tu_danh_sach if t in self.m.wv]
        if not ds: return None
        return np.mean(ds,axis=0)
    def tim_ngu_canh_lien_quan(self, v, top=5):
        if not self.kho_ngu_canh: return []
        arr = np.array([x["vec"] for x in self.kho_ngu_canh])
        sim = cosine_similarity([v], arr)[0]
        vi = np.argsort(sim)[::-1][:top]
        return [self.kho_ngu_canh[i]["tu"] for i in vi if sim[i]>0.22]
    def xoa_vector_lien_quan(self, v):
        if not v or not self.kho_ngu_canh: return
        arr=np.array([x["vec"] for x in self.kho_ngu_canh])
        sim=cosine_similarity([np.array(v)],arr)[0]
        self.kho_ngu_canh = [nc for nc,s in zip(self.kho_ngu_canh,sim) if s<0.85]
        self._luu()
