#!/data/data/com.termux/files/usr/bin/bash
echo "🔧 Đang cài đặt thư viện cần thiết..."
pkg update && pkg upgrade -y
pkg install python git clang python-numpy -y
pip install fastapi uvicorn pydantic gensim underthesea scikit-learn torch requests beautifulsoup4
echo "✅ Cài đặt hoàn tất! Đang khởi chạy hệ thống..."
cd ..
python xu-ly-ai/app.py
