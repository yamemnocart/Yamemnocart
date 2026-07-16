from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import sys
import os
sys.path.append(os.path.dirname(__file__))

from buoc1_etl import xu_ly_van_ban
from buoc2_vector import tao_vector, tim_tuong_thich
from buoc3_transformer import du_doan_cau_tra_loi
from phan_chia_du_lieu import chia_nho_van_ban
from che_do_phong_hoa import kiem_tra_che_do, chuyen_che_do_phong

app = FastAPI()

# Lưu trữ dữ liệu toàn cục
bo_nho_ai = {"vector": [], "van_ban": [], "lich_su_tra_loi": [], "so_lan_xoa": 0}

class CauHoi(BaseModel):
    cau_hoi: str

class VanBanNap(BaseModel):
    noi_dung: str

# Gắn giao diện web
app.mount("/static", StaticFiles(directory="../giao-dien"), name="giao_dien")

@app.get("/")
async def giao_dien_chat():
    return FileResponse("../giao-dien/index.html")

@app.get("/nap-du-lieu")
async def giao_dien_nap():
    return FileResponse("../giao-dien/nap-du-lieu.html")

@app.post("/api/nap-van-ban")
async def nhan_van_ban(van_ban: VanBanNap):
    try:
        # Chia nhỏ văn bản lớn
 doan_van = chia_nho_van_ban(van_ban.noi_dung)
        for doan in doan_van:
            # Làm sạch & tách từ
            du_lieu_sach = xu_ly_van_ban(doan)
            # Tạo vector nhúng từ
            vector_moi = tao_vector(du_lieu_sach)
            bo_nho_ai["vector"].extend(vector_moi)
            bo_nho_ai["van_ban"].extend(du_lieu_sach)
        return {"trang_thai": "thanh_cong", "thong_bao": "Đã nạp và xử lý dữ liệu thành công"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")

@app.post("/api/tra-loi")
async def tra_loi_cau_hoi(cau_hoi: CauHoi):
    try:
        # Kiểm tra chế độ hoạt động
        che_do = kiem_tra_che_do(bo_nho_ai["so_lan_xoa"])
        if che_do == "phong":
            chuyen_che_do_phong()

        # Xử lý câu hỏi
        du_lieu_cau_hoi = xu_ly_van_ban(cau_hoi.cau_hoi)
        vector_cau_hoi = tao_vector(du_lieu_cau_hoi)
        van_ban_lien_quan = tim_tuong_thich(vector_cau_hoi, bo_nho_ai["vector"], bo_nho_ai["van_ban"])
        cau_tra_loi = du_doan_cau_tra_loi(vector_cau_hoi, van_ban_lien_quan, che_do)

        bo_nho_ai["lich_su_tra_loi"].append(cau_tra_loi)
        return {"cau_tra_loi": cau_tra_loi}
    except Exception as e:
        return {"cau_tra_loi": "Tôi chưa hiểu câu hỏi này, vui lòng nạp thêm dữ liệu hoặc diễn đạt lại."}

@app.post("/api/xoa-cau-tra-loi")
async def xoa_cau_tra_loi_cuoi():
    if bo_nho_ai["lich_su_tra_loi"]:
        bo_nho_ai["lich_su_tra_loi"].pop()
        bo_nho_ai["so_lan_xoa"] += 1
        return {"trang_thai": "da_xoa", "thong_bao": "Đã xóa câu trả lời cuối cùng khỏi bộ nhớ"}
    return {"thong_bao": "Không có câu trả lời nào để xóa"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
