from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

html = """
<!doctype html>
<html>
<head>
    <title>Spothot - Connect to WiFi</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            text-align: center;
            width: 350px;
        }
        h1 {
            color: #333333;
            margin-bottom: 20px;
        }
        h2 {
            color: #666666;
            margin-bottom: 20px;
        }
        form {
            margin-top: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            color: #555555;
            font-weight: bold;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #cccccc;
            border-radius: 5px;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .spinner {
            display: none;
            margin: 20px auto;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #007bff;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .message {
            margin-top: 20px;
            color: #007bff;
            font-size: 16px;
            display: none;
        }
    </style>
    <script>
        function showSpinner() {
            document.getElementById('spinner').style.display = 'block';
            document.getElementById('message').style.display = 'block';
            document.getElementById('connectForm').style.display = 'none';
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Spothot</h1>
        <h2>Connect to WiFi</h2>
        <form id="connectForm" action="/" method="post" onsubmit="showSpinner()">
            <label for="ssid">SSID:</label>
            <input type="text" id="ssid" name="ssid" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <input type="submit" value="Connect">
        </form>
        <div id="spinner" class="spinner"></div>
        <div id="message" class="message">Connecting with your WiFi, please wait...</div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        connect_to_wifi(ssid, password)
    return render_template_string(html)

def connect_to_wifi(ssid, password):
    wpa_supplicant_conf = f"""
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="{ssid}"
    psk="{password}"
}}
"""
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
        f.write(wpa_supplicant_conf)

    os.system('sudo ifconfig wlan0 down')
    os.system('sudo ifconfig wlan0 up')
    os.system('sudo systemctl restart wpa_supplicant')
    os.system('sudo systemctl restart dhcpcd')
    os.system('sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf')

def run_flask():
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    run_flask()
