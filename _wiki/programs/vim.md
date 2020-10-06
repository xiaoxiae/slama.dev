---
---

### Command Mode

#### Shell
- `:sh` -- open shell (`Ctrl+D` to exit it)
- `:!` -- run a shell command

#### Autocomplete (insert mode)
- `Ctrl+n/p` -- jump to next/previous suggestion
- `Ctrl+y` -- accept suggestion
- `Ctrl+e` -- cancel suggestion
- `Ctrl+x` + `Ctrl+f` -- complete file name

#### Spellcheck
- `z=` -- autocomplete
- `]s` and `[s` -- next/previous misspelled word

#### Marky
- `m.`, kde `.` je znak (jako Ranger... tedy Ranger jako vim)
	- ' + <znak> -- skákání po značkách
	- `` -- skok zpět

#### Registry
- `"add` -- smaž a ulož do registru
- `.` -- text insertnut posledním insertem
- `*` -- clipboard
- `0-9` -- historie
- v insert módu: `<C-R>x` kde x je registr: paste

#### Miscellaneous
- `q:`, `q/`, `q?` -- history of previous commands and searches
- `Ctrl+a/x` -- increase/decrease the next number on the line

#### Tab Management
- `(v)sp <file>` -- (vertically) split open a file
	- alternatively (just split): `<C-W>v`/`<C-W>s`
- `Ctrl+w, h/j/k/l` -- move to the left/right/upper/lower tab

### Plugins

#### VimWiki
- `<leader>w`
    - `w` -- open wiki index file
    - `i` -- open diary index file
    - `s` -- select and open wiki index file
    - `d` -- delete the open wiki file
    - `r` -- rename the open wiki file
	- `<leader>w` - create a new diary entry with today

#### surround
- `ys` -- surround
    - `<movement>X` -- inner word with X
    - `sX` -- whole line with X
- `S` -- surround in visual mode
- `csXY` -- change surrounding X to Y
- `dsX` -- delete surrounding X
- `diX` -- delete _inside_ surrounding X
 
X (or Y) could mean a number of things:
- `)` or `b` -- round bracket
- `]` or `r` -- square bracket
- `}` or `B` -- curly brackets
- `>` -- <> thingys
- `` -- ``` thingys
- `'` -- single quotes
- `"` -- double quotes
- `t` -- HTML tag

#### dvim-multiple-cursors
- `Ctrl+n` (when something's selected) -- create new cursor at the match
- `Ctrl+p` -- remove the current virtual cursor
