import os
import subprocess
import argparse
from spothot.app import run_flask
import time

LOG_DIR = "/home/pi/"
LOG_FILE = os.path.join(LOG_DIR, "configure_hotspot.log")
WPA_SUPPLICANT_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"

# Ensure the necessary directories exist
def ensure_directory(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_log_directory():
    ensure_directory(LOG_FILE)

def log_message(message):
    ensure_log_directory()
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")
    print(message)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_message(f"Command '{command}' failed with error: {e}")

def is_wifi_configured():
    if os.path.exists(WPA_SUPPLICANT_CONF):
        with open(WPA_SUPPLICANT_CONF, 'r') as file:
            content = file.read()
            return 'ssid' in content and 'psk' in content
    return False

def clean_up_wpa_supplicant():
    # Kill any running wpa_supplicant instances to avoid conflicts
    run_command('sudo killall wpa_supplicant')

    # Remove stale wpa_supplicant control interfaces
    run_command('sudo rm -rf /var/run/wpa_supplicant/wlan0')

def connect_to_wifi(retries=3, wait_time=10):
    log_message("Attempting to connect to configured Wi-Fi...")

    clean_up_wpa_supplicant()

    # Start wpa_supplicant to connect to the Wi-Fi network
    run_command('sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf')

    for attempt in range(retries):
        log_message(f"Connection attempt {attempt + 1} of {retries}")
        # Request an IP address from the DHCP server
        run_command('sudo dhclient wlan0')

        # Check if connected to Wi-Fi
        try:
            subprocess.check_call(['ping -c 1 8.8.8.8'], shell=True)
            log_message("Connected to Wi-Fi successfully.")
            run_command('sudo systemctl restart dhcpcd')
            return True
        except subprocess.CalledProcessError:
            log_message("Failed to connect to Wi-Fi.")
            time.sleep(wait_time)

    log_message("All Wi-Fi connection attempts failed.")
    return False

def configure_network(ssid, password):
    log_message("Configuring network...")

    # Remove static IP configuration for wlan0 from dhcpcd.conf if it exists
    run_command('sudo sed -i \'/^interface wlan0$/,/^$/d\' /etc/dhcpcd.conf')

    # Create dnsmasq.conf configuration
    with open('/etc/dnsmasq.conf', 'w') as f:
        f.write("""
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
""")

    # Create hostapd.conf configuration
    with open('/etc/hostapd/hostapd.conf', 'w') as f:
        f.write(f"""
# Interface and driver settings
interface=wlan0
driver=nl80211

# Wi-Fi settings
ssid={ssid}
hw_mode=g
channel=10

# Security settings
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP

# Additional settings
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wmm_enabled=1

# Enable IEEE 802.11n (high throughput)
ieee80211n=1

# Optional: Enable Short Guard Interval for 802.11n
ht_capab=[SHORT-GI-20][HT20]
""")

    # Unmask hostapd service
    run_command('sudo systemctl unmask hostapd')

    # Correct the DAEMON_CONF line in /etc/default/hostapd
    run_command('sudo sed -i \'s|#DAEMON_CONF=".*"|DAEMON_CONF="/etc/hostapd/hostapd.conf"|\' /etc/default/hostapd')
    run_command('sudo sed -i \'s|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|g\' /etc/sysctl.conf')
    run_command('sudo sysctl -p')
    run_command('sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE')
    run_command('sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"')

def restart_services():
    log_message("Restarting services...")
    run_command('sudo systemctl restart dhcpcd')
    run_command('sudo systemctl restart dnsmasq')
    run_command('sudo systemctl restart hostapd')

def start_flask_app():
    log_message("Starting Flask app...")
    run_flask()

def main():
    parser = argparse.ArgumentParser(description="Setup Raspberry Pi as a Wi-Fi hotspot")
    parser.add_argument('--ssid', required=True, help='SSID for the Wi-Fi hotspot')
    parser.add_argument('--password', required=True, help='Password for the Wi-Fi hotspot')
    args = parser.parse_args()

    if os.geteuid() != 0:
        log_message("Please run the script with sudo.")
        exit(1)

    log_message("Starting process...")

    if is_wifi_configured() and connect_to_wifi():
        log_message("Connected to Wi-Fi successfully.")
    else:
        log_message("Could not connect to Wi-Fi. Setting up hotspot.")
        configure_network(args.ssid, args.password)
        restart_services()

    start_flask_app()

    log_message("Process completed.")

if __name__ == "__main__":
    main()