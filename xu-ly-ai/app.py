import os, sys, json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# ĐƯỜNG DẪN TUYỆT ĐỐI - CHẠY ĐÚNG MỌI NƠI BAO GỒM TERMUX
GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC/"xu-ly-ai"))

from buoc1_etl import lam_sach, tach_tu, luu_van_ban_goc
from buoc2_vector import Word2VecAI, khoi_tao_vector, tinh_tuong_dong_cosine
from buoc3_transformer import TransformerNho
from phan_chia_du_lieu import chia_thanh_doan_thong_minh
from che_do_phong_hoa import QuanLyCheDo

app = FastAPI(title="AI TỰ XÂY DỰNG")
app.mount("/giao-dien", StaticFiles(directory=str(GOC/"giao-dien")), name="gd")

# THƯ MỤC LƯU DỮ LIỆU
DL_GOC = GOC/"du-lieu"/"van-ban-goc"
DL_XL  = GOC/"du-lieu"/"du-lieu-da-xu-ly"
DL_MH  = GOC/"du-lieu"/"mo-hinh"
for p in [DL_GOC,DL_XL,DL_MH]: p.mkdir(parents=True,exist_ok=True)

# KHỞI TẠO MÔ HÌNH MỘT LẦN DUY NHẤ
w2v = Word2VecAI(DL_MH)
tf  = TransformerNho()
qld = QuanLyCheDo(nguong=5)
BO_NHO = {"lich_su":[]}

# === GIAO DIỆN ===
@app.get("/")
async def web_chat(): return FileResponse(str(GOC/"giao-dien"/"index.html"))
@app.get("/nap-du-lieu")
async def web_nap(): return FileResponse(str(GOC/"giao-dien"/"nap-du-lieu.html"))

# === API NẠP DỮ LIỆU ===
@app.post("/api/nap")
async def api_nap(rq:Request):
    j = await rq.json()
    nd = j.get("noi_dung","")
    cac_doan = chia_thanh_doan_thong_minh(nd, 450)
    luu_van_ban_goc(DL_GOC, nd)
    da_xu_ly = []
    for d in cac_doan:
        sach = lam_sach(d)
        tu   = tach_tu(sach)
        if len(tu)>=2: da_xu_ly.append(tu)
    # Lưu dữ liệu đã xử lý
    (DL_XL/"tu_da_tach.jsonl").open("a",encoding="utf8").write("\n".join(json.dumps(x,ensure_ascii=False) for x in da_xu_ly)+"\n")
    # Huấn luyện vector
    w2v.huan_luyen(da_xu_ly)
    return JSONResponse({"trang_thai":"ok","thong_bao":f"Đã chia {len(cac_doan)} đoạn → xử lý {len(da_xu_ly)} cụm từ → cập nhật bộ nhớ vector thành công"})

# === API TRẢ LỜI ===
@app.post("/api/hoi")
async def api_hoi(rq:Request):
    j = await rq.json()
    ch = j.get("cau_hoi","")
    ch_sach = lam_sach(ch)
    ch_tu   = tach_tu(ch_sach)
    if not ch_tu: return JSONResponse({"tra_loi":"⚠️ Câu hỏi quá ngắn hoặc không hợp lệ"})
    # Lấy chế độ hiện tại
    chedo = qld.che_do_hien_tai
    # Tạo vector câu hỏi
    vch = w2v.vector_cau(ch_tu)
    if vch is None: return JSONResponse({"tra_loi":"ℹ️ Chưa có dữ liệu nào, vui lòng nạp văn bản trước"})
    # Tìm ngữ cảnh gần nhất
    ngu_canh = w2v.tim_ngu_canh_lien_quan(vch, top=4)
    # Dự đoán qua Transformer
    tra_loi = tf.sinh_cau_tra_loi(ch_tu, ngu_canh, chedo)
    BO_NHO["lich_su"].append({"cau_hoi":ch_tu,"tra_loi":tra_loi,"vector":vch.tolist()})
    # Lưu lịch sử tạm
    (DL_MH/"lich_su_tra_loi.json").write_text(json.dumps(BO_NHO["lich_su"],ensure_ascii=False),encoding="utf8")
    return JSONResponse({"tra_loi":tra_loi,"che_do":chedo})

# === API XÓA - GỌI TỪ TERMINAL ===
@app.post("/api/xoa-cuoi")
async def xoa_cuoi():
    if not BO_NHO["lich_su"]: return JSONResponse({"tb":"Không có câu trả lời nào để xóa"})
    cuoi = BO_NHO["lich_su"].pop()
    w2v.xoa_vector_lien_quan(cuoi["vector"])
    qld.tang_dem()
    (DL_MH/"lich_su_tra_loi.json").write_text(json.dumps(BO_NHO["lich_su"],ensure_ascii=False),encoding="utf8")
    return JSONResponse({"tb":"✅ ĐÃ XÓA HOÀN TOÀN, AI SẼ KHÔNG BAO GIỜ NÓI LẠI NỘI DUNG NÀY","che_do_moi":qld.che_do_hien_tai})

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
