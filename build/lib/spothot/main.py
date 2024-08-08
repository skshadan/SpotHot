import os
import subprocess
import argparse
from spothot.app import run_flask

LOG_FILE = "/home/pi/configure_hotspot.log"

def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")
    print(message)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        log_message(f"Command '{command}' failed with error: {e}")

def configure_network(ssid, password):
    log_message("Configuring network...")

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

    run_command('sed -i \'s|#DAEMON_CONF="|DAEMON_CONF="/etc/hostapd/hostapd.conf"|g\' /etc/default/hostapd')
    run_command('sed -i \'s|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|g\' /etc/sysctl.conf')
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

    log_message("Starting hotspot configuration...")

    configure_network(args.ssid, args.password)
    restart_services()
    start_flask_app()

    log_message("Hotspot configuration completed.")

if __name__ == "__main__":
    main()
