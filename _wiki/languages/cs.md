---
title: C#
---

{% match ### Dictionaries %}
- `using System.Collections.Generic;`

| Action   | Code                                                   |
| ---      | ---                                                    |
| create   | `Dictionary<int, int> d = new Dictionary<int, int>();` |
| contains | `d.ContainsKey(element);`                              |
| add      | `d[index] = element;`                                  |

{% match ### Strings %}

| Action                       | Code                                                 |
| ---                          | ---                                                  |
| length                       | `s.Length;`                                          |
| split                        | `s.Split(char);`                                     |
| split on multiple delimiters | `s.Split(delimiters);`, `delimiters` jsou pole charů |

{% match ### Array %}

| Action          | Code                                                |
| ---             | ---                                                 |
| create          | `int[] array = new int[];`                          |
| fill with stuff | `Array.Fill(table, -1, 0, 256);`, requires `System` |

{% match ### Printing %}
- requires `System`

| Action            | Code                        |
| ---               | ---                         |
| print             | `Console.WriteLine(stuff);` |
| print w/o newline | `Console.Write(stuff);`     |


{% match ### Reading from files %}

| Action    | Code                                                              |
| ---       | ---                                                               |
| open      | `System.IO.StreamReader file = new System.IO.StreamReader(path);` |
| read line | `file.ReadLine()`                                                 |
| close     | `file.Close();`                                                   |

{% match ### Try/except %}
```cs
try {
	// stuff
} catch (Exception e) {
	// stuff
}
```

{% match ### Arithmetic overflows %}
```cs
checked {
	// kód
}
```
- is not controlled when functions are called from this block (how could it, when they're probably already translated...)
