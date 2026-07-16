import torch
import torch.nn as nn

kich_thuoc_dau_vao = 100
so_lop = 2
so_dau = 2

class MoHinhTransformer(nn.Module):
    def __init__(self):
        super().__init__()
        self.ma_hoa_vi_tri = nn.Parameter(torch.zeros(1, 512, kich_thuoc_dau_vao))
        self.bo_chuyen_doi = nn.TransformerEncoderLayer(d_model=kich_thuoc_dau_vao, nhead=so_dau, dim_feedforward=256)
        self.bo_ma_hoa = nn.TransformerEncoder(self.bo_chuyen_doi, num_layers=so_lop)
        self.tang_ra = nn.Linear(kich_thuoc_dau_vao, kich_thuoc_dau_vao)

    def forward(self, x):
        x += self.ma_hoa_vi_tri[:, :x.size(1)]
        return self.tang_ra(self.bo_ma_hoa(x))

mo_hinh_tf = MoHinhTransformer()

def du_doan_cau_tra_loi(vector_cau_hoi, van_ban_lien_quan, che_do="chinh"):
    if not van_ban_lien_quan:
        return "Tôi chưa có đủ dữ liệu để trả lời câu hỏi này."
    # Xử lý theo chế độ
    if che_do == "chinh":
        van_ban_gop = " ".join([" ".join(doan) for doan in van_ban_lien_quan[:3]])
    else:
        van_ban_gop = " ".join([" ".join(doan) for doan in van_ban_lien_quan[:1]])
    # Tạo câu trả lời đơn giản theo ngữ cảnh
    return f"Dựa trên dữ liệu tôi có: {van_ban_gop[:200]}..." if len(van_ban_gop) > 200 else f"Dựa trên dữ liệu tôi có: {van_ban_gop}"
