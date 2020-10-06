---
---

1. find the disk:  `sudo fdisk -l`
2. format to fat: `sudo mkfs.vfat /dev/sdb -I`
3. copy: `dd if=<path to image> of=/dev/sdb status=progress`

Note that `sdb` should be replaced with the correct disk.
