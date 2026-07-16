import os, sys, threading, subprocess, time
from pathlib import Path
GOC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC))

HOST="127.0.0.1"; PORT=8080
LINK_CHAT = f"http://{HOST}:{PORT}"
LINK_NAP  = f"http://{HOST}:{PORT}/nap-du-lieu"

def chay_may_chu():
    os.chdir(GOC/"xu-ly-ai")
    subprocess.run([sys.executable,"app.py"])

def menu_terminal():
    time.sleep(2.5)
    print("\n"+"="*50)
    print("🌐 HAI GIAO DIỆN ĐANG CHẠY:")
    print(f"  1) 💬 GIAO DIỆN CHAT CHÍNH  → {LINK_CHAT}")
    print(f"  2) 📥 GIAO DIỆN NẠP DỮ LIỆU → {LINK_NAP}")
    print("="*50)
    print("⌨️ LỆNH TRÊN NÀY ĐỂ SỬ DỤNG:")
    print("  xoa   → XÓA CÂU TRẢ LỜI CUỐI CÙNG VĨNH VIỄN")
    print("  thong → XEM THỐNG KÊ & CHẾ ĐỘ HIỆN TẠI")
    print("  stop  → DỪNG HỆ THỐNG HOÀN TOÀN")
    print("="*50)
    import urllib.request as u
    while True:
        try:
            l=input("\n⌨️ NHẬP LỆNH > ").strip().lower()
            if l=="xoa":
                r=u.urlopen(u.Request(f"{LINK_CHAT}/api/xoa-cuoi",method="POST")).read()
                print("👉",r.decode("utf8"))
            elif l=="thong":
                print(f"✅ Đang chạy ổn định | Link chat: {LINK_CHAT}")
            elif l=="stop":
                print("🛑 Đang tắt hệ thống..."); os._exit(0)
            else: print("❌ Lệnh không hợp lệ: dùng xoa / thong / stop")
        except KeyboardInterrupt: print("\n🛑 Thoát"); os._exit(0)
        except Exception as e: print("Lỗi:",e)

if __name__=="__main__":
    threading.Thread(target=chay_may_chu,daemon=True).start()
    menu_terminal()
