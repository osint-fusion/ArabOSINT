import os
import subprocess
from flask import Flask, render_template, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    target = data.get('target', '').strip()
    tool = data.get('tool', 'sherlock')

    if not target:
        return jsonify({'error': 'الرجاء إدخال هدف صحيح (يوزر، إيميل، أو رقم هاتف).'})

    result = ""
    try:
        if tool == 'sherlock':
            # تشغيل أداة Sherlock للبحث عن اليوزر
            process = subprocess.Popen(['sherlock', target, '--print-found'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            result = stdout if stdout else stderr

        elif tool == 'holehe':
            # تشغيل أداة Holehe للبحث عن حسابات الإيميل
            process = subprocess.Popen(['holehe', target, '--only-used'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            # تنظيف مخرجات Holehe لتكون مقروءة
            lines = stdout.split('\n')
            clean_output = "\n".join([line for line in lines if "[+]" in line or "Email used" in line])
            result = clean_output if clean_output else "لم يتم العثور على حسابات مرتبطة، أو حدث خطأ في الأداة.\n" + stderr

        elif tool == 'phone':
            # تشغيل مكتبة Phonenumbers لتحليل الرقم
            if not target.startswith('+'):
                target = '+' + target
            try:
                parsed_number = phonenumbers.parse(target)
                if phonenumbers.is_valid_number(parsed_number):
                    country = geocoder.description_for_number(parsed_number, "ar")
                    provider = carrier.name_for_number(parsed_number, "ar")
                    result = f"معلومات الرقم: {target}\nالبلد/المنطقة: {country}\nمزود الخدمة: {provider}\nالرقم صالح: نعم"
                else:
                    result = "الرقم غير صالح. تأكد من إدخال الرقم بشكل صحيح مع رمز الدولة."
            except Exception as e:
                result = f"خطأ في تحليل الرقم: تأكد من كتابة الرقم بالصيغة الدولية (+964...)\nالتفاصيل: {str(e)}"
        else:
            result = "الأداة المحددة غير صالحة."

    except FileNotFoundError as fnf:
        result = f"الأداة المطلوبة غير مثبتة أو غير موجودة في المسار.\nالتفاصيل: {str(fnf)}"
    except Exception as e:
        result = f"حدث خطأ أثناء التنفيذ:\n{str(e)}"

    return jsonify({'result': result})

if __name__ == '__main__':
    # إنشاء مجلد templates تلقائياً إذا لم يكن موجوداً
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(host='127.0.0.1', port=5000, debug=True)