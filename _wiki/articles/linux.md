---
---

Random notes for (Arch/Manjaro) Linux-related things that I don't use often enough to remember well, or just want them written down.

### Useful commands

| command       | description                          | misc.                                                                |
| ---           | ---                                  | ---                                                                  |
| `chroot`      | change the apparent root directory   |                                                                      |
| `cut`         | cut file/stdin using a delimiter     | `-d.`-- delimiter, `-f` -- field                                     |
| `echo`        | display a string of text             | `-e` -- enable backslash escapes                                     |
| `find`        | find all the things that you lost    | `-type c` -- _d_irectory/_f_ile/_l_ink (symbolic), `-name 'pattern'` |
| `grep`        | print lines that match patterns      | `-i` -- ignore case, `-r` -- recursive, `-E` -- extended regexp      |
| `ls`          | list directory contents              | `-a` --- hidden files, `l` -- mode info                              |
| `mkdir`       | create a directory                   | `-p` -- create parents too                                           |
| `passwd`      | change the password of a user        | `passwd <user>` as root -- change password of the user               |
| `paste`       | merge lines of files                 | `-d` -- delimiter, `-s` -- paste one file at a time                  |
| `pr`          | paginate (prepare for printing)      |                                                                      |
| `read`        | read to variable                     |                                                                      |
| `sed`         | edit stuff                           | `-i` -- edit files in-place                                          |
| `shuf`        | shuffle (generate permutation of)    |                                                                      |
| `ssh-copy-id` | copy a key to the destination server | `-i` -- which key to use                                             |
| `ssh-keygen`  | generate keys for SSH                | `-C` -- comment, `-p -f <key>` -- change password                    |
| `tr`          | translate/delete characters          | `-c`                                                                 |
| `wc`          | number of _ in a file/files          | `-c/m/l` for bytes, chars, newlines                                  |
| `w`           | who is currently using this machine  | `-f` -- where from, `-i` -- IP                                       |
| `xargs`       | build arguments for a command        |                                                                      |

### `ssh`
- `-L <[from]:port:to:port>` -- redirect client sockets to given host address and port
- `-R <[from]:port:to:port>` -- redirect host sockets to given client address and port
- `-J <comma separated destinations>` -- jump through here first
- `-i` -- which identity file to use
- `-N` -- do not execute a remote command, only forward
- `-X` -- forward X

### Pipefail
`set pipefail` -- fail the command pipe on various conditions:
- `-e` -- unknown command
- `-u` -- non-zero exit code of anything
- `-o` -- unknown (unset) variable

### Command chaining
- `;` -- just a delimiter
- `&&` -- run if previous exit code was non-zero
- `||` -- run if previous exit code was zero

### Virtual terminals
From Arch Linux wiki: _The console is presented to the user as a series of virtual consoles. These give the impression that several independent terminals are running concurrently; each virtual console can be logged in with different users, run its own shell and have its own font settings. The virtual consoles each use a device /dev/ttyX, and you can switch between them by pressing Alt+Fx (where x is equal to the virtual console number, beginning with 1). The device /dev/console is automatically mapped to the active virtual console._

- `ctrl + alt + F<number>` -- change to a given virtual console (`/dev/tty<number>`)

### Disk partitioning with `fdisk`

#### Flags
- `fdisk -l` (maybe with sudo) -- list connected disks

#### Commands
- `p` -- print current partitions
- `n` -- new partition
- `t` -- change partition type
- `l` -- list partition types
- `w` -- save and quit
- don't forget to do both root and aux when installing new devices!


### [Magic SysRq key](https://en.wikipedia.org/wiki/Magic_SysRq_key)
- performing various low-level command regardless of the system's state
- REISUB (safe reboot, mainly those last 3 things):
- un`R`aw (take control of keyboard back from X)
- t`E`rminate (send SIGTERM to all processes, allowing them to terminate gracefully)
- k`I`ll (send SIGKILL to all processes except init, forcing them to terminate immediately)
- `S`ync (flush data to disk)
- `U`nmount (remount all filesystems read-only)
- re`B`oot
- hack: `echo <command> > /proc/sysrq-trigger`

### `rsync`
- `-a` -- archive mode
	- perserves modified time, user+group, permussions...
- `-v` -- increased verbosity
- `-z` -- compress data during a transfer

### NTP with `timedatectl`
- `sudo timedatectl set-ntp true`, when the `ntp` package is installed

### Multiple failed password attempt lock
- `sudo vim /etc/security/faillock.conf`, set `deny=0`
- useful when you have a new keyboard you're not used to :P

### Hardware

#### What is currently connected?
- `lsusb` -- USB devices
- `lspci` -- PCI devices
- `lsblk` -- block devices
	- `sudo fdisk -l` and `df -h` are somewhat related

#### Full specs with `inxi`
- `-F` -- full
- `-a` -- alternate kernel modules
- `-z` -- filter for sensitive information
- `-i` -- show WAN IP

### Other resources
- [ext3 vs. ext4](https://askubuntu.com/questions/44908/what-is-the-difference-between-ext3-ext4-from-a-generic-users-perspectiv)
