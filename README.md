
![Logo](https://github.com/skshadan/SpotHot/blob/main/images/spothot.png?raw=true)


# Spothot
Spothot is a Python package that transforms your Raspberry Pi into a Wi-Fi hotspot with an intuitive Flask web interface. Users can easily set up and manage the hotspot directly through their web browser, making it a perfect solution for portable Wi-Fi needs or network testing.




## Features
- Simple Setup: Quickly configure your Raspberry Pi as a Wi-Fi hotspot.
- Web Interface: Manage hotspot settings directly through an easy-to-use web interface.
- Flexible Configuration: Specify the SSID and password for your hotspot via command line arguments.


## Installation


```bash
 sudo apt-get update
 sudo apt-get upgrade
```
```bash
 sudo apt-get install dnsmasq hostapd python3-flask
```
```bash
 pip install spothot
```
or

```bash
 sudo apt-get install dnsmasq hostapd python3-flask dhcpcd5 iptables && sudo pip install spothot
```












    
## Usage
To set up the Wi-Fi hotspot, use the following command:
### Replace YourSSID and YourPassword with your desired network name and password.
```bash
  sudo spothot --ssid YourSSID --password YourPassword
```


## Running on Boot
To ensure that Spothot runs on boot, add the following line to your /etc/rc.local file before the exit 0 line:
```bash
  sudo nano /etc/rc.local
```
```bash
  sudo spothot --ssid YourSSID --password YourPassword &
```

![Logo](https://github.com/skshadan/SpotHot/blob/main/images/wifi.png?raw=true)






## Facing Any Issues?

Contributions are welcome! Please feel free to submit a Pull Request or open an issue.

## License

[MIT](https://choosealicense.com/licenses/mit/)


## fin.