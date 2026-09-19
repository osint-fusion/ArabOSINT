cat << 'EOF' > app.py
from flask import Flask, render_template, request, jsonify
import subprocess
import concurrent.futures
import re
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = Flask(__name__)

def run_cmd(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"[!] خطأ أثناء تشغيل الأمر: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', mode=['POST'], methods=['POST'])
def search():
    data = request.get_json()
    target = data.get('target', '').strip()
    country_code = data.get('country_code', '').strip()
    scan_type = data.get('scan_type', '')

    if not target:
        return jsonify({'error': 'يرجى إدخال الهدف أولاً.'})

    full_phone = f"{country_code}{target.lstrip('0')}" if country_code and scan_type in ['phone_info', 'phone_to_email'] else target

    output = f"=== [ ArabOSINT v2.0 - تقرير الفحص الموحد ] ===\n"
    output += f"[*] الهدف المحدد: {full_phone}\n"
    output += f"[*] نوع العملية: {scan_type}\n"
    output += "="*50 + "\n\n"

    # تشغيل الأدوات بالتوازي لتسريع العملية
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []

        if scan_type in ['email_search', 'email_info', 'email_to_phone', 'full_scan']:
            futures.append(executor.submit(run_cmd, f"holehe {target}"))
            futures.append(executor.submit(run_cmd, f"h8mail -t {target}"))
            futures.append(executor.submit(run_cmd, f"socialscan {target}"))

        if scan_type in ['phone_info', 'phone_to_email', 'full_scan']:
            # تحليل رقم الهاتف بالمكتبة المباشرة
            try:
                parsed_num = phonenumbers.parse(full_phone, None)
                if phonenumbers.is_valid_number(parsed_num):
                    geo = geocoder.description_for_number(parsed_num, "ar")
                    car = carrier.name_for_number(parsed_num, "ar")
                    tz = timezone.time_zones_for_number(parsed_num)
                    phone_analysis = f"[+] الدولة/المنطقة: {geo}\n[+] شركة الاتصالات: {car}\n[+] النطاق الزمني: {tz}\n"
                    results.append("=== [ تحليل رقم الهاتف - Phone Analysis ] ===\n" + phone_analysis)
            except Exception as e:
                results.append(f"[!] خطأ في تحليل الرقم: {str(e)}\n")

            futures.append(executor.submit(run_cmd, f"phoneinfoga scan -n {full_phone}"))

        if scan_type in ['username_search', 'full_scan']:
            user_target = target.split('@')[0]
            futures.append(executor.submit(run_cmd, f"maigret {user_target} --timeout 10 -a"))
            futures.append(executor.submit(run_cmd, f"sherlock {user_target} --timeout 10"))

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                results.append(res)

    output += "\n".join(results)
    return jsonify({'result': output})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
EOF
