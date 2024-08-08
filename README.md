# Spothot

**Spothot** is a Python package that transforms your Raspberry Pi into a Wi-Fi hotspot with an intuitive Flask web interface. Users can easily set up and manage the hotspot directly through their web browser, making it a perfect solution for portable Wi-Fi needs or network testing.

## Features

- **Simple Setup:** Quickly configure your Raspberry Pi as a Wi-Fi hotspot.
- **Web Interface:** Manage hotspot settings directly through an easy-to-use web interface.
- **Flexible Configuration:** Specify the SSID and password for your hotspot via command line arguments.

## Installation

To install Spothot, simply run:

pip install spothot

## Usage

To set up the Wi-Fi hotspot, use the following command:

spothot --ssid YourSSID --password YourPassword

Replace YourSSID and YourPassword with your desired network name and password.

## Configuration

### Command Line Arguments

- --ssid: Specifies the SSID (network name) for the Wi-Fi hotspot.
- --password: Specifies the password for the Wi-Fi hotspot.

### Example

spothot --ssid MyHotspot --password MySecretPassword

## Running on Boot

To ensure that Spothot runs on boot, add the following line to your /etc/rc.local file before the exit 0 line:

sudo spothot --ssid YourSSID --password YourPassword &

Replace YourSSID and YourPassword with your desired network name and password.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue.

## License

This project is licensed under the MIT License.
