import os
import subprocess
import argparse
from spothot.app import run_flask

LOG_DIR = "/home/pi/"
LOG_FILE = os.path.join(LOG_DIR, "configure_hotspot.log")

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

def run_command(command, retry_on_failure=False):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_message(f"Command '{command}' failed with error: {e}")
        if retry_on_failure and "hostapd" in command:
            log_message("Attempting to resolve wpa_supplicant conflict and retrying...")
            resolve_wpa_supplicant_conflict()
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                log_message(f"Retry failed with error: {e}")

def resolve_wpa_supplicant_conflict():
    log_message("Stopping wpa_supplicant to avoid conflicts with hostapd...")
    run_command('sudo systemctl stop wpa_supplicant')
    log_message("Bringing wlan0 interface down and up again...")
    run_command('sudo ifconfig wlan0 down')
    run_command('sudo ifconfig wlan0 up')

def configure_network(ssid, password):
    log_message("Configuring network...")

    # Ensure directories exist before writing configuration files
    ensure_directory('/etc/hostapd')
    ensure_directory('/etc/dnsmasq.d')
    ensure_directory('/etc')

    # Create dhcpcd.conf configuration
    with open('/etc/dhcpcd.conf', 'w') as f:
        f.write("""
# Static IP configuration for wlan0
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
""")

    # Create dnsmasq.conf configuration
    with open('/etc/dnsmasq.conf', 'w') as f:
        f.write("""
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
""")

    # Create hostapd.conf configuration
    with open('/etc/hostapd/hostapd.conf', 'w') as f:
        f.write(f"""
interface=wlan0
driver=nl80211
ssid={ssid}
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
""")

    # Correct the DAEMON_CONF line in /etc/default/hostapd
    run_command('sudo sed -i \'s|DAEMON_CONF=".*"|DAEMON_CONF="/etc/hostapd/hostapd.conf"|\' /etc/default/hostapd')
    run_command('sudo sed -i \'s|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|g\' /etc/sysctl.conf')
    run_command('sudo sysctl -p')
    run_command('sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE')
    run_command('sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"')

def restart_services():
    log_message("Restarting services...")
    run_command('sudo systemctl restart dhcpcd')
    run_command('sudo systemctl restart dnsmasq')
    run_command('sudo systemctl restart hostapd', retry_on_failure=True)

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

    log_message("Starting hotspot configuration...")

    configure_network(args.ssid, args.password)
    restart_services()
    start_flask_app()

    log_message("Hotspot configuration completed.")

if __name__ == "__main__":
    main()
