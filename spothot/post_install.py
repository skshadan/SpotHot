import subprocess
import sys
import platform

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}", file=sys.stderr)
        sys.exit(1)

def fix_dpkg():
    print("Checking for dpkg issues...")
    try:
        run_command('sudo dpkg --configure -a')
    except:
        print("Failed to fix dpkg, please manually run 'sudo dpkg --configure -a'.", file=sys.stderr)
        sys.exit(1)

def install_required_packages():
    if platform.system() == 'Linux':
        required_packages = ['hostapd', 'iptables', 'dhcpcd5', 'dnsmasq']
        
        fix_dpkg()  # First, fix any dpkg issues

        for package in required_packages:
            try:
                print(f"Installing {package}...")
                run_command(f'sudo apt-get install -y {package}')
            except:
                print(f"Failed to install {package}.", file=sys.stderr)
                sys.exit(1)
    else:
        print("Skipping system package installation because this is not a Linux system.")

if __name__ == "__main__":
    install_required_packages()
