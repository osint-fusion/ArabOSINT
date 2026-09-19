# ArabOSINT

أداة تجميع معلومات واستخبارات مفتوحة المصدر (OSINT) بواجهة ويب رسومية (GUI) تعمل محلياً (Localhost).
تم تصميم الأداة لتسهيل عمل الباحثين الأمنيين من خلال دمج أقوى أدوات الـ OSINT في واجهة واحدة دون الحاجة لحفظ أوامر الـ Terminal.

## الأدوات المدمجة حالياً:
1. **Sherlock**: للبحث عن أسماء المستخدمين (Usernames) عبر مئات المنصات.
2. **Holehe**: لمعرفة المواقع والحسابات المرتبطة بعنوان البريد الإلكتروني (Email).
3. **Phonenumbers**: لتحليل أرقام الهواتف دولياً وجلب بيانات المنطقة ومزود الخدمة.

## طريقة التثبيت على (Kali Linux / Ubuntu / Debian)
افتح التيرمينال واكتب الأوامر التالية بالترتيب:

```bash
# 1. نسخ المستودع
git clone [https://github.com/YOUR_USERNAME/ArabOSINT.git](https://github.com/YOUR_USERNAME/ArabOSINT.git)
cd ArabOSINT

# 2. إعطاء الصلاحيات لسكربت التثبيت وتشغيله
chmod +x setup.sh
./setup.sh