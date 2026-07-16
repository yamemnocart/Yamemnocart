#!/data/data/com.termux/files/usr/bin/bash
clear
echo "========================================="
echo "    🚀 KHỞI CHẠY HỆ THỐNG AI TỪ GỐC"
echo "========================================="
cd "$(dirname "$0")/.."
export PIP_BREAK_SYSTEM_PACKAGES=1

echo "[1/4] Cập nhật hệ thống..."
pkg update -y -o Dpkg::Options::="--force-confdef" 2>/dev/null

echo "[2/4] Cài môi trường..."
pkg install -y python git clang libopenblas python-numpy 2>/dev/null

echo "[3/4] Cài thư viện Python..."
pip install --quiet fastapi uvicorn requests beautifulsoup4 lxml gensim underthesea scikit-learn
pip install --quiet torch --index-url https://download.pytorch.org/whl/cpu 2>/dev/null || pip install --quiet torch

echo "[4/4] Khởi động quản lý web..."
chmod +x cong-cu/quan-ly-web.py
python cong-cu/quan-ly-web.py
