#!/bin/bash
echo "[+] جاري إعداد بيئة ArabOSINT..."

# التحقق من وجود python3-venv وتثبيته إذا لم يكن موجوداً
if ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "[!] حزمة python3-venv غير موجودة. جاري التثبيت (قد يتطلب كلمة مرور الجذر)..."
    sudo apt-get update && sudo apt-get install python3-venv -y
fi

echo "[+] إنشاء البيئة الافتراضية (Virtual Environment)..."
python3 -m venv venv

echo "[+] تفعيل البيئة الافتراضية..."
source venv/bin/activate

echo "[+] تثبيت الأدوات والمكتبات الأساسية (Flask, Sherlock, Holehe, Phonenumbers)..."
pip install --upgrade pip
pip install -r requirements.txt

echo "=================================================="
echo "[+] تم التثبيت بنجاح!"
echo "[+] لتشغيل الأداة في أي وقت، اتبع الخطوتين التاليتين:"
echo "1. source venv/bin/activate"
echo "2. python3 app.py"
echo "=================================================="