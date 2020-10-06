---
---

- instalace Dokuwiki, Apache, PHP
- úprava `/etc/httpd/conf/extra/dokuwiki.conf`:

```
order allow,deny
allow from all
```
na
{:.center}
```
Require all granted
```
- přidání Dokuwiki do `/etc/httpd/conf/httpd.conf`

```
Include conf/extra/dokuwiki.conf
```

- přidání PHP do Apache (změna `/etc/httpd/conf/httpd.conf`)
	- comment    `LoadModule mpm_event_module modules/mod_mpm_event.so`
	- uncmomment `LoadModule mpm_prefork_module modules/mod_mpm_prefork.so`
	- přidat na konec `LoadModule` listu:

```
LoadModule php7_module modules/libphp7.so
AddHandler php7-script .php
```

- přidat na konec `Include` listu (na konec souboru):

```
Include conf/extra/php7_module.conf
```

- restart Apache (`systemctl restart httpd.service`)
