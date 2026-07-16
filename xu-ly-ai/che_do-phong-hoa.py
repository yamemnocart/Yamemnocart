def kiem_tra_che_do(so_lan_xoa):
    # Nếu xóa hơn 5 lần tự chuyển chế độ phòng
    return "chinh" if so_lan_xoa < 5 else "phong"

def chuyen_che_do_phong():
    print("⚠️ Hệ thống chuyển sang chế độ phòng ngừa: Giảm độ phức tạp, trả lời ngắn gọn hơn")
