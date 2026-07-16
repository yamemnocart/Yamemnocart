import torch, torch.nn as nn, math
torch.set_num_threads(2) # TỐI ƯU CHO ĐIỆN THOẠI

class ViTri(nn.Module):
    def __init__(self,d,maxlen=256):
        super().__init__()
        pe=torch.zeros(maxlen,d)
        p=torch.arange(0,maxlen,dtype=torch.float).unsqueeze(1)
        k=torch.exp(torch.arange(0,d,2).float()*(-math.log(10000)/d))
        pe[:,0::2]=torch.sin(p*k); pe[:,1::2]=torch.cos(p*k)
        self.register_buffer('pe',pe.unsqueeze(0))
    def forward(self,x): return x+self.pe[:,:x.size(1)]

class TransformerNho(nn.Module):
    def __init__(self,d=128,dau=4,sau=128,lop=1):
        super().__init__()
        self.vt=ViTri(d)
        enc=nn.TransformerEncoderLayer(d_model=d,nhead=dau,dim_feedforward=sau,batch_first=True,dropout=0.05)
        self.tr=nn.TransformerEncoder(enc,num_layers=lop)
    def forward(self,x):
        return self.tr(self.vt(x))
    def sinh_cau_tra_loi(self, cau_hoi, ngu_canh, chedo="chinh"):
        if not ngu_canh:
            return "Tôi chưa học nội dung này. Vui lòng nạp văn bản liên quan vào hệ thống rồi hỏi lại nhé."
        gop = []
        for nc in ngu_canh: gop.extend(nc)
        # Loại trùng
        gop2=[]
        for t in gop:
            if t not in gop2: gop2.append(t)
        if chedo=="chinh":
            do_dai=220
            noi=" ".join(gop2)
            if len(noi)>do_dai: noi=noi[:do_dai].rsplit(" ",1)[0]+"..."
            return f"Dựa trên dữ liệu bạn cung cấp:\n👉 {noi}"
        else:
            # CHẾ ĐỘ PHÒNG: RÚT GỌN CHỈ TỪ KHÓA CHÍNH
            return "📌 "+" - ".join(gop2[:12])
