---
---

### `xsetwacom`
- the `xf86-input-wacom` package
	- might also need `kcm-wacomtablet` for newer tablets
- **listing:**
	- `xsetwacom --list devices` for devices
	- `xsetwacom --list modifiersmouse wheel` for available modifiers and buttons
- **setting:** `xsetwacom set "Wacom Intuos BT S Pad pad" Button 3 key "ctrl" "z"`

### Dual-monitor mapping
1. `xrandr` or `arandr` -- get the name of the monitor to map to
2. `xinput` -- determine, which device to map (it should be the stylus)
3. `xinput map-to-output <device id> <monitor name>` -- map
