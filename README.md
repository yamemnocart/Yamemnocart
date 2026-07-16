# 🤖 AI TỰ XÂY DỰNG TỪ CON SỐ 0
Chạy hoàn toàn trên điện thoại Android qua Termux, dùng HTML+CSS+JS+Python, gồm ETL → Word2Vec → Transformer tự lập trình.

## Cấu trúc
- `giao-dien/` → 2 trang web
- `xu-ly-ai/` → Toàn bộ logic AI
- `du-lieu/` → Dữ liệu gốc, đã xử lý, mô hình
- `cong-cu/khoi-chay.sh` → Chạy một lệnh là xong

## Cài đặt & chạy trên Termux
```bash
pkg install git -y
git clone LINK_GITHUB_CUA_BAN du-an-ai-tu-goc
cd du-an-ai-tu-goc
chmod +x cong-cu/khoi-chay.sh
./cong-cu/khoi-chay.sh
