import re
from underthesea import word_tokenize

def xu_ly_van_ban(noi_dung):
    # Xóa thẻ HTML
    noi_dung = re.sub(r'<[^>]+>', '', noi_dung)
    # Xóa ký tự đặc biệt, khoảng trắng thừa
    noi_dung = re.sub(r'[^\w\s.?!,àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', ' ', noi_dung)
    noi_dung = re.sub(r'\s+', ' ', noi_dung).strip()
    if not noi_dung:
        return []
    # Tách từ tiếng Việt
    cau_hoa = word_tokenize(noi_dung, format="text")
    return cau_hoa.split()
