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

{% match #### Inheritance %}
```cs
class A { }      // some stuff
class B : A { }  // some stuff + some more stuff

A a = new A(); // is fine
a = new B();   // is also fine
```

- when inheriting, everything is inherited, **except constructors**
	- it would be a mess -- which constructor would get called when
- each class has **exactly one** predecessor
	- if none is specified, `System.Object == object` is used automatically

##### `System.Object`
```cs
class Object {
	protected object MemberwiseClone() {}
	public Type GetType() {}
	public virtual bool Equals(object o) {}
	public virtual string ToString() {}
	public virtual int GetHashCode() {}
	public static bool ReferenceEquals(object objA, object objB) {}
	
}
```

#### `sealed`
- prevence dědičnosti
- `sealed class` -- není inheritovatelná
- `sealed void MojeFunkce()` -- není overridovatelná


{% match ### Variable scope %}

{% match #### Local variables %}
- created each time we enter `{`, deleted each time we leave `}`
	- but... is extremely fast (1 instruction) and can be optimized by the compiler, if a variable is repeatedly created and discarded
- the same name can't be reused within the same scope, but:

```cs
if <something> {int b;} else {int b;}  // this is ok
int b;  // this is not (already declared in a nested block)
```

- also, the compiler must know that the variable is initialized before use
	- a hack is to assign something garbage to f (and add a comment)

```cs
int e = 1, f;
if (e == 1) {f = 2;}
e = f; // error, f is not initialized in all paths
```

{% match ### Exceptions %}
- all exceptions must inherit the `Exception` class
- takes a _long_ time (a lot of things have to be collected)
	- a simple `try` block is basically free, though
- watch out for things like `StackOverflow` -- some exceptions can't be caught

| Function     | Meaning                                  |
| ---          | ---                                      |
| e.Message    | error message as a `string`              |
| e.StackTrace | trace of method call stack as a `string` |
| e.StackTrace | trace of method call stack as a `string` |
| e.ToString   | the formatted exception `string`         |

#### Syntax
```cs
try {
	// stuff
} catch (Exception e) {
	// stuff only executed if the type matches the exception raised
} finally {
	// stuff always executed
	// for example, for closing IO/network resources
}
```

#### `using` 
```cs
using (type x = new Type()) {
	// some code
}
```
- is equivalent to

```cs
Type x;
try {
	x = new Type();  // could raise an exception!
	
	// some code
} finally {
	if (x != null) x.Dispose();
}
```

- is also equivalent to (since C# 8.0)
	- the `Dispose` is called when the variable goes out of scope

```cs
using type x = new Type();
```

- only works with objects that are **disposable** (inherit `IDisposable` {% latex %}\implies{% endlatex %} have a `Dispose` method)

### Properties

```cs
int Property {
	get { /* stuff to do */ }
	set { /* stuff to do (with a variable `value`) */ }
}
```

- syntactic sugar for defining a `int get` and `void set` methods
	- must be used with `=` though, although it does internally generate methods `get_X` and `set_X`
- `set` takes `value` as the only parameter
	- "value" is a keyword only in the setter
- is nice when we want to let the programmer know that we're just setting/getting something (although it may do something more complex)
- also nice when internally having a variable that we don't want the user to access
	- integers that are smaller than 50 and divisible by 3 -- setting will cause an exception (would be a pain to debug if the variable was public)
- interfaces can also contain them!
- **auto-implemented properties**: if we're just doing `get => value` and `set = value`, we can just do `get;` and `set;` and this code will get automatically generated
	- what if we want to make an interface out of it in the future?
	- what if we want to add constraints to the values in the future?

### `=>`
- syntactic sugar for:
	- when a non-`void` method returns something
	- when a void method has only one command
- also **works for getters and setters!**

### `ref`
```cs
void Inc(ref int x) { x += 1; }

void f() {
	int val = 3;
	Inc(ref val);  // val will be 4
}
```

- call **by reference**
- address is passed and automatically de-referenced
- parameter must be a variable, not an expression (what would that even mean?)
- makes sense if we really want to modify the passed variable

#### `out`
```cs
void Read(out int first, out int next) {
	first = Console.Read();
	next = Console.Read();
}

void f() {
	int first, next;
	Read(out first, out next);
}
```

- similar to `ref`, but no value is passed by the caller
- useful for returning/setting multiple things in a function
- each `out` parameter must have a value assigned by the time it leaves the function
	- no solution if we want to not assign the variables (assign dummy values...)
- the variable can be declared as a part of the function call

```cs
int a;
if (tryParse(something, out a)) { print("We failed: " + a); }
print("We didn't fail: " + a);

// <=>

if (tryParse(something, out int a)) { print("We failed: " + a); }
print("We didn't fail: " + a);

// <=>

if (tryParse(something, out var a)) { print("We failed: " + a); }
print("We didn't fail: " + a);
```

### `var`
- derived at compile time, depending on what is on the right side
- if we can't determine the type, the code won't compile
	- `var x;`
	- `var y = (1, 2, 3);`
	- `var z = null`
- the declaration is a comment -- it's unwise to write `var` everywhere:
	- `var name = GetName();     // what does this return?`
	- `var d = new List<int>();  // what if I want to change List to a HashSet later?`

### Interfaces
- a "contract" for classes to follow
	- we can assign any class that implements an interface to variables with an interface (when we only require the functionality of the interface)
- can't be instantiated
- not entirely an abstract class -- classes can implement multiple interfaces
	- (interfaces can also implement interfaces)

### Abstract classes
- sort of like interfaces, but with code
- we can define default members and methods that all classes inheriting this one will use

### Other

#### Arithmetic overflows
```cs
checked {
	// kód
}
```
- is not controlled when functions are called from this block (how could it, when they're probably already translated...)

#### Commenting trick
```cs
/*/  // adding a * here uncomments the code

code

/**/
```

#### `nameof(x)` [Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/operators/nameof)
- name of `x`:
- useful when debugging, when showing exceptions to users...

```cs
Console.WriteLine(nameof(System.Collections.Generic));  // output: Generic
Console.WriteLine(nameof(List<int>));                   // output: List
Console.WriteLine(nameof(List<int>.Count));             // output: Count
Console.WriteLine(nameof(List<int>.Add));               // output: Add

var numbers = new List<int> { 1, 2, 3 };
Console.WriteLine(nameof(numbers));        // output: numbers
Console.WriteLine(nameof(numbers.Count));  // output: Count
Console.WriteLine(nameof(numbers.Add));    // output: Add
```
