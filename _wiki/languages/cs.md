---
title: C#
---

### Dictionaries
- `using System.Collections.Generic;`

| Action   | Code                                                   |
| ---      | ---                                                    |
| create   | `Dictionary<int, int> d = new Dictionary<int, int>();` |
| contains | `d.ContainsKey(element);`                              |
| add      | `d[index] = element;`                                  |

### Strings

| Action                       | Code                                                 |
| ---                          | ---                                                  |
| length                       | `s.Length;`                                          |
| split                        | `s.Split(char);`                                     |
| split on multiple delimiters | `s.Split(delimiters);`, `delimiters` jsou pole charů |

### Array 

| Action          | Code                                                |
| ---             | ---                                                 |
| create          | `int[] array = new int[];`                          |
| fill with stuff | `Array.Fill(table, -1, 0, 256);`, requires `System` |

### Arguments
- are in `main`'s `string[] args`, ya dingus

### Reading from files

| Action    | Code                                                              |
| ---       | ---                                                               |
| open      | `System.IO.StreamReader file = new System.IO.StreamReader(path);` |
| read line | `file.ReadLine()`                                                 |
| close     | `file.Close();`                                                   |

### Try/except
```cs
try {
	// stuff
} catch (Exception e) {
	// stuff
}
```

### Arithmetic overflows
```cs
checked {
	// kód
}
```
- is not controlled when functions are called from this block (how could it, when they're probably already translated...)


