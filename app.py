import os
import subprocess
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    target = data.get('target', '').strip()
    tool = data.get('tool', '').strip()

    if not target or not tool:
        return jsonify({"error": "⚠️ يرجى إدخال البيانات المطلوبة كاملة."})

    try:
        # 1. فحص أسماء المستخدمين عبر Sherlock
        if tool == 'sherlock':
            cmd = ['sherlock', target, '--timeout', '10']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            output = result.stdout if result.stdout else result.stderr
            return jsonify({"result": output if output else "لم يتم العثور على نتائج."})

        # 2. فحص البريد الإلكتروني عبر Holehe
        elif tool == 'holehe':
            cmd = ['holehe', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            output = result.stdout if result.stdout else result.stderr
            return jsonify({"result": output if output else "لم يتم العثور على حسابات مرتبطة."})

        # 3. تحليل بيانات أرقام الهواتف عبر Phonenumbers
        elif tool == 'phone':
            parsed_num = phonenumbers.parse(target)
            if phonenumbers.is_valid_number(parsed_num):
                region = geocoder.description_for_number(parsed_num, "ar") or geocoder.description_for_number(parsed_num, "en")
                net_carrier = carrier.name_for_number(parsed_num, "ar") or carrier.name_for_number(parsed_num, "en")
                time_zones = timezone.time_zones_for_number(parsed_num)
                
                report = f"📞 --- تقرير فحص الرقم الدولي ---\n\n"
                report += f"🔹 الرقم المفحوص: {target}\n"
                report += f"🌍 الدولة / المنطقة: {region if region else 'غير معروف'}\n"
                report += f"🏢 الشركة المزودة للخدمة: {net_carrier if net_carrier else 'غير متاح'}\n"
                report += f"⏰ المنطقة الزمنية: {', '.join(time_zones)}\n"
                report += f"✅ حالة الرقم: صحيح وفعال رسمياً\n"
                return jsonify({"result": report})
            else:
                return jsonify({"error": "❌ الرقم المدخل غير صحيح أو لا يطابق الصيغة الدولية."})

        else:
            return jsonify({"error": "الأداة المحددة غير مدعومة."})

    except subprocess.TimeoutExpired:
        return jsonify({"error": "⏱️ انتهت مهلة الفحص، حاول مرة أخرى."})
    except Exception as e:
        return jsonify({"error": f"❌ حدث خطأ أثناء التنفيذ: {str(e)}"})

if __name__ == '__main__':
    print("🚀 جاري تشغيل سيرفر ArabOSINT على http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
