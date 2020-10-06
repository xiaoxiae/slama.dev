---
---

### Short list of useful commands

| command       | description                            | misc.                                                                |
| ---           | ---                                    | ---                                                                  |
| `cat`         | print to stdout                        |                                                                      |
| `read`        | read to variable                       |                                                                      |
| `chroot`      | change the apparent root directory     |                                                                      |
| `cut`         | cut file/stdin using a delimiter       | `-d.`-- delimiter, `-f` -- field                                     |
| `diff`        | compare files                          | `--color=always`                                                     |
| `echo`        | display a string of text               | `-e` -- enable backslash escapes                                     |
| `fdisk`       | format disks                           |                                                                      |
| `find`        | find all the things that you lost      | `-type c` -- _d_irectory/_f_ile/_l_ink (symbolic), `-name 'pattern'` |
| `grep`        | print lines that match patterns        | `-i` -- ignore case, `-r` -- recursive, `-E` -- extended regexp      |
| `head`        | output the first part of files         | `-n/c` -- first n lines/bytes                                        |
| `ls`          | list directory contents                | `-a` --- hidden files, `l` -- mode info                              |
| `mkdir`       | create a directory                     | `-p` -- create parents too                                           |
| `mkfs.ext4`   | create ext4 filesystem on a given disk |                                                                      |
| `paste`       | merge lines of files                   | `-d` -- delimiter, `-s` -- paste one file at a time                  |
| `pr`          | paginate (prepare for printing)        |                                                                      |
| `sed`         | stream editor                          | `-i` -- edit files in-place                                          |
| `shuf`        | shuffle (generate permutation of)      |                                                                      |
| `ssh`         | SSH                                    |                                                                      |
| `ssh-keygen`  | generate keys for SSH                  | `-C` -- comment, `-p -f <key>` -- change password                    |
| `ssh-copy-id` | copy key to the destination derver     |                                                                      |
| `tail`        | output the last part of files          | `-n/c` -- last n lines/bytes                                         |
| `tr`          | translate/delete characters            | `-c`                                                                 |
| `wc`          | number of _ in a file/files            | `-c/m/l` for bytes, chars, newlines                                  |
| `w`           | who is currently using this machine    | `-f` -- where from, `-i` -- IP                                       |
| `xargs`       | build arguments for a command          |                                                                      |

### SSH
- `-L <[from]:port:to:port>` -- redirect client sockets to given host address and port
- `-R <[from]:port:to:port>` -- redirect host sockets to given client address and port
- `-J <comma separated destinations>` -- first jump here
- `-i` -- which identity file to use
- `-N` -- do not execute a remote command, only forward

### Pipefail
`set pipefail` -- fail the command pipe on various conditions:
- `-e` -- unknown command
- `-u` -- non-zero exit code of anything
- `-o` -- unknown (unset) variable

### Command chaining
 - `;` -- just a delimiter
 - `&&` -- run if previous exit code was non-zero
 - `||` -- run if previous exit code was zero

### What do parentheses do?
```
if [ CONDITION ]    Test construct  
if [[ CONDITION ]]  Extended test construct  
Array[1]=element1   Array initialization  
[a-z]               Range of characters within a Regular Expression
$[ expression ]     A non-standard & obsolete version of $(( expression )) [1]


${variable}                             Parameter substitution
${!variable}                            Indirect variable reference
{ command1; command2; . . . commandN; } Block of code
{string1,string2,string3,...}           Brace expansion
{a..z}                                  Extended brace expansion
{}                                      Text replacement, after find and xargs


( command1; command2 )             Command group executed within a subshell
Array=(element1 element2 element3) Array initialization
result=$(COMMAND)                  Command substitution, new style
>(COMMAND)                         Process substitution
<(COMMAND)                         Process substitution


(( var = 78 ))            Integer arithmetic
var=$(( 20 + 5 ))         Integer arithmetic, with variable assignment
(( var++ ))               C-style variable increment
(( var-- ))               C-style variable decrement
(( var0 = var1<98?9:21 )) C-style ternary operation
```

### Virtual terminals
From Arch Linux wiki: _The console is presented to the user as a series of virtual consoles. These give the impression that several independent terminals are running concurrently; each virtual console can be logged in with different users, run its own shell and have its own font settings. The virtual consoles each use a device /dev/ttyX, and you can switch between them by pressing Alt+Fx (where x is equal to the virtual console number, beginning with 1). The device /dev/console is automatically mapped to the active virtual console._

### Keyboard shortcuts
- `ctrl + alt + F<number>` -- change to a given virtual console (`/dev/tty<number>`)
- `alt + ←` -- shell po startu systému

### Disk Partitioning and formatting
Some notes on partitioning disks for new system installations.

#### fdisk
Creating partitions on certain disks

##### Flags
- `fdisk -l` (maybe with sudo) -- list connected disks

##### Commands
- `p`: print current partitions
- `n`: new partition
- `t`: change partition type
	- `l` -- list partition types
- `w`: save and quit
- don't forget to do both root and aux when installing new devices!

#### mkfs.ext4
Creating the ext4 file system on a given disk.

#### resources
- [ext3 vs. ext4](https://askubuntu.com/questions/44908/what-is-the-difference-between-ext3-ext4-from-a-generic-users-perspectiv)

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

### Rsync
- `-a` -- archive mode
	- zachová modified time, user+group, permussions...
- `-v` -- increased verbosity
- `-z` -- compress data during a transfer
