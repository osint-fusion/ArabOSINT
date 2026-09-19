#!/bin/bash

echo "=================================================="
echo "[+] جاري إعداد وتحديث بيئة أداة ArabOSINT..."
echo "=================================================="

# إنشاء البيئة الافتراضية إذا لم تكن موجودة
if [ ! -d "venv" ]; then
    echo "[+] إنشاء البيئة الافتراضية (Virtual Environment)..."
    python3 -m venv venv
fi

# تفعيل البيئة الافتراضية
echo "[+] تفعيل البيئة الافتراضية..."
source venv/bin/activate

# تحديث مدير الحزم pip وتثبيت المكتبات
echo "[+] تثبيت وتحديث جميع أدوات ومكتبات OSINT..."
pip install --upgrade pip
pip install -r requirements.txt

# إنشاء مجلد templates إذا لم يكن موجوداً
mkdir -p templates

echo "=================================================="
echo "[+] تم إعداد وتثبيت جميع الأدوات بنجاح!"
echo "[+] لتشغيل الأداة استخدم الأوامر التالية:"
echo "    source venv/bin/activate"
echo "    python3 app.py"
echo "=================================================="
EOF
