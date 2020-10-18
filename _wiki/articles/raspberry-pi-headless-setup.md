---
---

- download Raspbian lite image
- [format the SD card](/wiki/articles/bootable-usb-drive-using-dd)
- create `wpa_supplicant.conf` with the following content (replacing the `<...>` stuff):

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<ISO 3166-1 country code>

network={
 ssid="<name>"
 psk="<password>"
}
```
- create a file called `ssh`
- use `nmap` to find the IP of the RPI
	- use `-sn` to not scan ports
- note: default name is `pi`, default password is `raspberry`
