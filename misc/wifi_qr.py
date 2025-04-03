import argparse
import qrcode

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--ssid", required=True, help="SSID of the Wi-Fi network")
ap.add_argument("-p", "--password", required=True, help="Password for the Wi-Fi network")
ap.add_argument("-o", "--output", default="wifi_qr.png", help="Output filename for the QR code")
args = ap.parse_args()

img = qrcode.make("WIFI:T:WPA;S:{SSID};P:{PASSWORD};H:false;;".format(
    SSID=args.ssid,
    PASSWORD=args.password,
))
img.save(args.output)

