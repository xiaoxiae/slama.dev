---
---

### Příkazy
- `new` -- zapnutí sessiony
	- `-s <jméno>` -- jméno
	- `-d` -- rovnou detatchni
- `ls` -- vypsání sessionů
- `attach` -- attachnutí se k (poslednímu?) sessionu
	- `-s <jméno>` -- jméno
- `send-keys <klávesy>` -- poslání kláves do sessionu
	- `-s <jméno>` -- jméno
	- `-t <pane>` -- číslo panu
- `split-window` 
	- `-h` -- horizontálně
- `pipe-pane` 
	- `-o <příkaz>`
	- `-t <pane>` -- číslo panu

### Klávesy (`C-b` + .)
- `c`: nové okno
- `d`: detatch
- `w`: vyber okno (interaktivně)
- `0`: přepni do okna
- `%/"`: splitni horizontálně/vertikálně

### Misc.
- oddělování příkazů jde přes `\;`
