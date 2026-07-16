const formNhap = document.getElementById('form-nhap');
const oNhap = document.getElementById('o-nhap');
const khungChat = document.getElementById('khung-chat');

formNhap.addEventListener('submit', async (e) => {
    e.preventDefault();
    const cauHoi = oNhap.value.trim();
    if (!cauHoi) return;

    // Thêm câu hỏi người dùng
    themTinNhan(cauHoi, 'nguoi');
    oNhap.value = '';

    // Hiển thị trạng thái chờ
    const taiKhoan = themTinNhan('Đang phân tích...', 'ai');

    // Gửi yêu cầu đến máy chủ
    try {
        const phanHoi = await fetch('/api/tra-loi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cau_hoi: cauHoi })
        });
        const duLieu = await phanHoi.json();
        taiKhoan.querySelector('.noi-dung').textContent = duLieu.cau_tra_loi;
    } catch (loi) {
        taiKhoan.querySelector('.noi-dung').textContent = 'Lỗi kết nối đến hệ thống AI!';
    }
});

function themTinNhan(noiDung, loai) {
    const div = document.createElement('div');
    div.className = `tin-nhan ${loai}`;
    div.innerHTML = `<div class="noi-dung">${noiDung}</div>`;
    khungChat.appendChild(div);
    khungChat.scrollTop = khungChat.scrollHeight;
    return div;
}
