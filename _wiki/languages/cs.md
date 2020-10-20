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

| Action                       | Code                                                 |
| ---                          | ---                                                  |
| length                       | `s.Length;`                                          |
| split                        | `s.Split(char);`                                     |
| split on multiple delimiters | `s.Split(delimiters);`, `delimiters` jsou pole charů |
| convert to integer           | `int.Parse(string);`                                 |

#### `System.Text.StringBuilder`
- "mutable string"
- internally behaves like a dynamic array (amortized resize)
- quick operations like concatenation
- `.ToString()` returns a proper string (since we can't use `StringBuilder` anywhere we want a string)
	- no copying happens -- internally, the new string points to the contents of the `StringBuilder` (so we don't have to copy twice)
		- if we were to modify again, it does actually get copied

#### Interpolation
- `Console.Write("cislo = {0} a {1}", i, j");`
	- same as `Console.Write("cislo = " + i.ToString() + " a " + j.ToString())`,
	- calls `String.Format("format string", i, j)`
		- creates new string
- careful:

```cs
Console.WriteLine("{0}: Hello, {1}!", s1, s2);
Console.WriteLine("{0}: Hello, " + s2 + "!", s1, s2);  // what if s2 == "{0}"
```

- **interpolated strings** -- `$"My name is {name} and I'm {age}."`
	- is translated into a `String.Format` call (at compile time)
	- the `{}` blocks can contain `:fmt` and `, fmt`
		- sometimes better to surround with `()` (ternary...)
	- if assigned to a `FormattableString`, an instance is created instead
		- `.GetArgument(i)` returns the i-th argument
		- `.Format()` creates a string

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

{% match ### Classes %}

{% match #### Constructor %}
- same syntax as C++, but add `public` before it
- if none is specified, a default one without parameters is created
	- we have to write it explicitly if we want it besides a parametered one

```cs
class A {
	int x = stuff;
	
	A () {}
}

// is equivalent to (for each constructor!)
// stuff can be any code, not just literals

class A {
	A () {
		int x = stuff;
	}
}
```

- when inheriting, the constructor of the predecesor should be called
	- actually, everything inherits `: object` (if not inheriting anything)
		- actually, `object == System.Object`

```cs
class A : Z {
	int x = something;
	
	A () {stuff}
}

// is equivalent to (for each constructor!)
// stuff can be any code, not just literals

class A : Z {
	A () {
		int x = something;
		
		// constructor of Z
		
		stuff
	}
}
```

- which constructor of the predecessor is called?
	- the one without parameters is called by default (it has to exist!)... or:

```cs
class A : Z {
	A () : base(/*parameters for constructor of Z*/) {stuff}
}

// is equivalent to (for each constructor!)
// stuff can be any code, not just literals

class A : Z {
	A () {
		int x = something;
		
		// constructor of Z
		
		stuff
	}
}
```

- calling one constructor from another constructor:
	- `A(): this(constructor parameters) {}`
	- the stuff that would be called before `A()` isn't
- **class constructors**:
	- called before the first time an object of the class is created
	- same as a regular constructor but for static variables
	- if none is specified, a default blank one is created

```cs
class A {
	static A() {}
}
```



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

### ???
```cs
/*/  // adding a * here uncomments the code

code

/**/
```
