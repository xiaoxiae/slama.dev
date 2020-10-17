---
title: C#
---

{% match ### Data structures %}

{% match #### Arrays %}

| Action          | Code                                                |
| ---             | ---                                                 |
| create          | `int[] array = new int[];`                          |
| fill with stuff | `Array.Fill(table, -1, 0, 256);`, requires `System` |

{% match #### Dictionaries %}
- `using System.Collections.Generic;`

| Action   | Code                                                   |
| ---      | ---                                                    |
| create   | `Dictionary<int, int> d = new Dictionary<int, int>();` |
| contains | `d.ContainsKey(element);`                              |
| add      | `d[index] = element;`                                  |

{% match #### Queues %}

| Action | Code                                         |
| ---    | ---                                          |
| create | `Queue<string> q = new Queue<string>();`     |
| add    | `q.Enqueue(element);`                        |
| pop    | `q.Dequeue(element);`                        |
| size   | `q.Count;`                                   |
| peek   | `q.Peek();`                                  |

{% match ### Strings %}
- `System.String` == `string` (keyword)
	- can't ever be a name of a variable!
	- what if someone decides to implement a `String` class
		- `string` removes the confusion
- internally an array of chars
- dynamically allocated on the heap
	- happens for each new string!
	- **string interning** -- hashmap for reusing already created strings
		- only for constants, not variables (only exception being `""`)!
		- we can do this ourselves using `String.Intern(str);` -- if the table contains it, return it; else add it to the table
			- limited use: strings can't be removed from the table
- **immutable** (neither length nor contents)
	- concatenation creates new strings
		- `String.concat(s1, s2, s3, ...);` is good for concatenating a lot of them
			- `s = "a" + "bcd" + "ef";` uses this method, so it isn't slow
- lives on the heap as long as there are pointers to it
	- if nothing points to it, it is garbage-collected
- `==` compares contents, char by char (same as `.Equals()`)
	- we can use `object.ReferenceEquals(o1, o2)` if we want reference equality

#### `System.Text.StringBuilder`
- "mutable string"
- internally behaves like a dynamic array (amortized resize)
- quick operations like concatenation
- `.ToString()` returns a proper string (since we can't use `StringBuilder` anywhere we want a string)
	- no copying happens -- internally, the new string points to the contents of the `StringBuilder` (so we don't have to copy twice)
		- if we were to modify again, it does actually get copied

| Action                       | Code                                                 |
| ---                          | ---                                                  |
| length                       | `s.Length;`                                          |
| split                        | `s.Split(char);`                                     |
| split on multiple delimiters | `s.Split(delimiters);`, `delimiters` jsou pole charů |
| convert to integer           | `int.Parse(string);`                                 |

{% match ### Chars %}
- `System.Char` == `char` (keyword)
- 2-byte UTF-16 character
	- some characters must be at least a string, since some UTF-16 characters can be up to 4 bytes


{% match ### Printing %}
- requires `System`

| Action            | Code                        |
| ---               | ---                         |
| print             | `Console.WriteLine(stuff);` |
| print w/o newline | `Console.Write(stuff);`     |

{% match ### File I/O %}

| Action     | Code                                                              |
| ---        | ---                                                               |
| reading    | `System.IO.StreamReader f = new System.IO.StreamReader(path);`    |
| read line  | `f.ReadLine();`                                                   |
| read chars | `int chars_read = f.Read(buffer, 0, BUFFER_SIZE);`                |
| writing    | `System.IO.StreamWriter f = new System.IO.StreamWriter(path);`    |
| write line | `f.WriteLine(line);`                                              |
| close      | `f.Dispose();`                                                    |

{% match ### Try/except %}
```cs
try {
	// stuff
} catch (Exception e) {
	// stuff
}
```

#### `var`
- odvození v době překladu podle toho, co je na pravé straně
- `string`, pole `int`ů...
- pokud to při překladu nejde zjistit, tak to nejde:
	- `var x;`
	- `var y = (1, 2, 3);`
	- `var z = null`
- deklarace je komentář -- `var` psát všude není rozumný:
	- `var name = GetName();  // co tohle vrací?`
- když budu chtít změnit implementaci, tak chci spíš:
	- `var d = new List<int>();  // co když pak budu chtít změnit na HashSet?`

### Arithmetic overflows
```cs
checked {
	// kód
}
```
- is not controlled when functions are called from this block (how could it, when they're probably already translated...)
