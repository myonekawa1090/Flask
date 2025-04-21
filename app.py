from flask import Flask, render_template, request
import time
from typing import Optional
from datetime import datetime

app = Flask(__name__)

MAX_SLEEP_TIME = 6000  # スリープ時間の上限（秒）
HEALTH_CHECK_TIMEOUT = 5  # ヘルスチェックのタイムアウト（秒）

def get_client_ip() -> str:
    """安全にクライアントIPを取得する"""
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    return request.remote_addr

def format_headers(headers) -> dict:
    """
    HTTPヘッダーを見やすく整形する
    重要なヘッダーを優先的に表示し、整理された形で返す
    """
    important_headers = {
        'User-Agent': headers.get('User-Agent', ''),
        'Accept': headers.get('Accept', ''),
        'Accept-Language': headers.get('Accept-Language', ''),
        'X-Forwarded-For': headers.get('X-Forwarded-For', ''),
        'X-Real-IP': headers.get('X-Real-IP', ''),
        'Host': headers.get('Host', ''),
        'Referer': headers.get('Referer', ''),
    }
    
    # その他のヘッダーを追加
    other_headers = {
        k: v for k, v in headers.items() 
        if k not in important_headers
    }
    
    return {
        'important': important_headers,
        'other': other_headers
    }

@app.route('/')
def hello_world():
    ip = get_client_ip()
    baseurl = request.base_url
    formatted_headers = format_headers(request.headers)
    
    # シンプルモードの判定
    is_simple_mode = request.args.get('mode') == 'simple'
    
    if is_simple_mode:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status_code = 200
        return f"{current_time} - IP: {ip} - Status: {status_code}", status_code
    
    return render_template('index.html', 
                         ip=ip, 
                         baseurl=baseurl, 
                         headers=formatted_headers)

@app.route('/contents/index.html')
def contents():
    ip = get_client_ip()
    baseurl = request.base_url
    formatted_headers = format_headers(request.headers)
    return render_template('contents.html', 
                         ip=ip, 
                         baseurl=baseurl, 
                         headers=formatted_headers)

@app.route('/size/')
def size():
    try:
        size_param = request.args.get('v')
        if size_param is None or not size_param.isnumeric():
            if request.args.get('mode') == 'simple':
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ip = get_client_ip()
                return f"{current_time} - IP: {ip} - Status: 200", 200
            return render_template('size.html', size=1)
        size_value = max(1, min(int(size_param), 100))  # 1から100の範囲に制限
        if request.args.get('mode') == 'simple':
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = get_client_ip()
            return f"{current_time} - IP: {ip} - Status: 200", 200
        return render_template('size.html', size=size_value)
    except ValueError:
        if request.args.get('mode') == 'simple':
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = get_client_ip()
            return f"{current_time} - IP: {ip} - Status: 200", 200
        return render_template('size.html', size=1)

@app.route('/sleep/')   
def sleep():
    try:
        sleep_param = request.args.get('v')
        if sleep_param is None or not sleep_param.isnumeric():
            time.sleep(1)
            if request.args.get('mode') == 'simple':
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ip = get_client_ip()
                return f"{current_time} - IP: {ip} - Status: 200", 200
            return render_template('sleep.html', time=1)
        
        sleep_time = min(int(sleep_param), MAX_SLEEP_TIME)  # 上限を設定
        time.sleep(sleep_time)
        if request.args.get('mode') == 'simple':
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = get_client_ip()
            return f"{current_time} - IP: {ip} - Status: 200", 200
        return render_template('sleep.html', time=sleep_time), 200
    except ValueError:
        time.sleep(1)
        if request.args.get('mode') == 'simple':
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = get_client_ip()
            return f"{current_time} - IP: {ip} - Status: 200", 200
        return render_template('sleep.html', time=1)

@app.route('/health/')   
def health():
    time.sleep(HEALTH_CHECK_TIMEOUT)
    return 'OK', 200

if __name__ == '__main__':
    # 本番環境では環境変数から設定を読み込むことを推奨
    debug_mode = False  # 本番環境ではFalseに
    port = 4996
    app.run(
        debug=debug_mode,
        port=port,
        host='0.0.0.0'  # すべてのインターフェースでリッスン
    )
