class QuanLyCheDo:
    def __init__(self, nguong=5):
        self.nguong=nguong
        self.so_lan_xoa=0
    @property
    def che_do_hien_tai(self):
        return "phong" if self.so_lan_xoa >= self.nguong else "chinh"
    def tang_dem(self):
        self.so_lan_xoa+=1
        if self.so_lan_xoa==self.nguong:
            print("\n⚠️ ⚠️ ⚠️ BẠN ĐÃ XÓA NHIỀU LẦN → HỆ THỐNG TỰ ĐỘNG CHUYỂN SANG CHẾ ĐỘ PHÒNG NGỪA ⚠️ ⚠️ ⚠️\n")
    def dat_lai(self): self.so_lan_xoa=0
