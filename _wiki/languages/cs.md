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
- internally an array of chars
- **immutable** (neither length nor contents)
	- concatenation creates new strings
		- `String.concat(s1, s2, s3, ...);` is good for concatenating a lot of them
			- `s = "a" + "bcd" + "ef";` uses this method, so it isn't slow
- `System.String` == `string` (keyword)
	- can't ever be a name of a variable!
	- what if someone decides to implement a `String` class
		- `string` removes the confusion
- dynamically allocated on the heap
	- happens for each new string!
	- **string interning** -- hashmap for reusing already created strings
		- only for constants, not variables (only exception being `""`)!
		[-](-) we can do this ourselves using `String.Intern(str);` -- if the table contains it, return it; else add it to the table
			- limited use: strings can't be removed from the table
- lives on the heap as long as there are pointers to it
	- if nothing points to it, it is garbage-collected
- `==` compares contents, char by char (same as `.Equals()`)
	- we can use `object.ReferenceEquals(o1, o2)` if we want reference equality

| Action                       | Code                                             |
| ---                          | ---                                              |
| length                       | `s.Length;`                                      |
| split                        | `s.Split(char);`                                 |
| split on multiple delimiters | `s.Split(delimiters);`, `delimiters` is `char[]` |
| convert to integer           | `int.Parse(string);`                             |

#### `System.Text.StringBuilder`
- "mutable string"
- internally behaves like a dynamic array (amortized resize)
- quick operations like concatenation
- `.ToString()` returns a proper string (since we can't use `StringBuilder` anywhere we want a string)
	- no copying happens -- internally, the new string points to the contents of the `StringBuilder` (so we don't have to copy twice); if we were to modify the string builder again, it does actually get copied

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
	- is translated into a `String.Format` call (at compile time)... most of the time
		- if assigned to a `FormattableString`, its instance is created instead
			- `.GetArgument(i)` returns the i-th argument
			- `.Format()` creates a string
	- the `{}` blocks can contain `:fmt` and `, fmt`
		- sometimes better to surround with `()` (ternary...)

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

- if we're dealing with binary I/O, use `FileStream` instead; this is for text

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
- same syntax as C++, but it's a good idea to add a `public` before it
- if none is specified, a default one without parameters is created
	- note that we have to write it explicitly if we want it besides one with parameters!
- translated to a `.ctor` method (see disassembly)
	- useful to know, since debug messages can contain this

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

- everything in C# inherits `: object` (if not inheriting anything)
	- `object == System.Object`, same as for strings
- when inheriting, the constructor of the predecessor is called like this:

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

- if no constructor without parameters exist, the code wouldn't compile, so we have to specify the correct constructor like this:
	- we can also just do so if we want to call a different one, even if one without parameters exists

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
	- the stuff that would be called before `A()` isn't called (so we don't call something, that we want to call once, twice)

{% match #### Class constructor %}
- same as a regular constructor but for static variables
- called before the first time an object of the class is created
	- if no object is constructed, it is never called
	- if we do `Class a;`, then it's also not called!
- if none is specified, a default blank one is created
	- this means that it can never have parameters
- called `.cctor`

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
	- it would be a mess -- which constructor would get called when?
- each class has **exactly one** predecessor
	- if none is specified, `System.Object == object` is used automatically

##### Superclass to subclass conversion
- take `A` and `B` from the code above; if we do `B b = (B)a;`, then this has to be checked at runtime
	- the conversion is explicit, because it's something to think about
- if it's wrong `InvalidCastException` is thrown, so test the code!
- can be written explicitly  

###### `is`
- checks, whether `object` is of the given `Type` (or type of any of its children)
- runtime calls a method, not too quick of an operation -- has to go through the entire class tree!
- if `object` is `null`, `false` is always returned

###### `as`
- returns the `object` if it is of the given `Type` (or type of any of its children), else `null`

```cs
B b = a as B;  // assigns `a` to `b` if it's of the valid type
               // this is the reason why `null is A` returns false

if (b != null) {
	// do stuff with `B b`
}

// is almost equivalent to (since C# 7.0)

if (a is B b) {
	// do stuff with `B b`
}

// `b` is not initialized here!
```

##### `System.Object`
- inherited by all classes
- has the following members:
	- `protected object MemberwiseClone();`
		- creates a shallow copy of the object (byte by byte)
		- doesn't make much sense for reference types
		- note that it is protected!
			- implement `public A Clone() {...}` to make it public
			- there is an `IClonable` interface, but it was before `<T>`...
	- `public Type GetType();`
		- done for all types (`new Type("A")`,...)
		- contains `.Name` and other stuff for reflection
		- also contains a **virtual method table**
	- `public virtual bool Equals(object o);`
	- `public virtual string ToString();`
		- the string representation of the object
		- shouldn't be something too complicated (like a giant recursive function)
	- `public virtual int GetHashCode();`
		- hash code of the object; for hashmap-like data structures
	- `public static bool ReferenceEquals(object objA, object objB);`
		- whether the two objects are equal by reference

##### `System.ValueType`
- is inherited by all types (`int`, `Nullable`, `bool`, user-defined structures...)
- overrides `Equals` to be byte-equal (since it is a value type)
	- if it has reference members, **uses reflection to check their values too** -- string, for example
		- better to implement it ourselves in this case

##### `sealed`
- prevents inheritance and (likely) allows for some code optimizations
	- no virtual function calls
- `sealed class` -- is not inherited
- `sealed void MyFunction()` -- is not overridable

{% match ### Variable scope %}

{% match #### Local variables %}
- created each time we enter `{`, deleted each time we leave `}`
	- but... is extremely fast and can be optimized by the compiler, if a variable is repeatedly created and discarded
- the same name can't be reused within the same scope, but be careful:

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
	- even the ones from other languages are wrapped in a `SEHException`
- takes a _long_ time (a lot of things have to be collected)
	- a simple `try` block is basically free, though
- watch out for exceptions that 
	- can't be caught (like `StackOverflowException`)
	- probably shouldn't be caught (like `OutOfMemoryException`)

| Property/Function | Meaning                             |
| ---               | ---                                 |
| e.Message         | `string` error message              |
| e.StackTrace      | `string` trace of method call stack |
| e.Source          | `string` app/object that threw it   |
| e.ToString()      | `string` the formatted exception    |

#### Syntax
```cs
try {
	// stuff
} catch (Exception e) {
	// stuff only executed if the type matches the exception raised
} finally {
	// stuff always executed, even if the exception is not handled
	// for example, for closing IO/network resources
}
```

### Common exceptions
- it's important to distinguish exceptions due to bugs (`NullReferenceException`, `IndexOutOfRangeException`) and due to incorrect program usage (possibly `FileNotFoundException`)

- `Exception`
	- `SystemException`
		- `ArithmeticException`
			- `DivideByZeroException`
			- `OverflowException`
			- ....
		- `NullReferenceException`
		- `IndexOutOfRangeException`
		- `InvalidCastException`
		- ...
	- `ApplicationException`
		- user-defined exceptions
		- ...
	- `IOException`
		- `FileNotFoundException`
		- `DirectoryNotFoundException`
		- ...
	- `WebException`
	- ...


### `using`
```cs
Type x;
try {
	x = new Type();  // could raise an exception!
	
	// some code
} finally {
	if (x != null) x.Dispose();
}
```
- is (sort of, because `x` has a slightly different scope) equivalent to

```cs
using (type x = new Type()) {
	// some code
}

// is also equivalent to (since C# 8.0)
// the `Dispose` is called when the variable goes out of scope

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
	- must be used with `=`, although it does internally generate methods `get_X` and `set_X`
- `set` takes `value` as the only parameter
	- "value" is a keyword only in the setter
- is nice when we want to let the programmer know that we're just setting/getting something (although it may do something more complex)
	- it's generally a good idea to not make it too slow, since the programmer expects it to be instant
-  when doing assemblies, properties make it so we don't need to rebuild code that uses it, since the API stays the same
- also nice when internally having a variable that we don't want the user to access
	- integers that are smaller than 50 and divisible by 3 -- setting will cause an exception (would be a pain to debug if the variable was public)
- interfaces can also contain them (not the implementation, just that it has to have a getter)!
- **auto-implemented properties**: if we're just doing `get => value` and `set = value`, we can just do `get;` and `set;` and this code will get automatically generated
	- what if we want to make an interface out of it in the future?
	- what if we want to add constraints to the values in the future?
- we can also set default values: `int X { get; set; } = 12;`
- we can also explicitly set the scope of the functions: `public int Length { get; private set; }`
	- `public` affects `get`, since it doesn't have an explicit modifier, but not `set`, because it has one

#### Creating objects with properties
```cs
A a = new A { x = 3; y = 6 };

// is literally the same as

A a = new A();
a.x = 3;
a.y = 6;
```

#### Parametric properties (indexers)
- for defining indexing on the class
- can be overloaded, since it's just a method (but might not always be the smartest thing to do!)
- be careful -- indexers, properties and events are compiled into „normal“ methods
	- `get_*` and `set_*` (property getter/setter)
	- `get_Item` and `set_Item` (indexer getter/setter)

```cs
class File {
	FileStream s;
	
	public int this [int index] {
		get {
			s.Seek(index, SeekOrigin.Begin);
			return s.ReadByte();
		}
		
		set {
			s.Seek(index, SeekOrigin.Begin);
			return s.WriteByte((byte) value);
		}
	}
	
}
```

### CLI Type System
- compared to C++, we can't choose whether something is a value or a reference, since it is determined by the type
- assignment is dependent on the type, so:
	- assigning value **copies it**
	- assigning reference **creates a new reference to it**

#### Value types
- variable is always the **value**
- allocated **in-place** (with exceptions)
- contains:
	- structures
		- simple types
		- nullables
		- user-defined structures
	- enumerations
- `new` can also be used, but it **doesn't allocate anything** -- it just calls the empty constructor
	- is weird, since it's completely different to references that are allocated

#### Reference types
- variable is always the **reference**
- the actual value is allocated on **managed heaps**
- can only ever be assigned a reference to the heap
- can contain a `null`
	- actually, since C# 8.0, we can toggle this behavior and forbid it to contain a `null`
		- gives warnings, because there can be paths where it isn't `null` but compiler doesn't see it
		- this makes it so we can make it `Nullable` using `?` too
- contains:
	- classes
	- interfaces
	- arrays
	- delegates
- more memory
	- the reference itself
	- **heap overhead**
		1. which type it is (reference to an instance of the class `MethodTable`)
			- is either {% latex %}4/8B{% endlatex %}, depending on the architecture
		2. syncblock -- related to threads and locking
			- always {% latex %}4B{% endlatex %}
		- padded to nearest {% latex %}8B{% endlatex %}

| Type           | Variables | Instances |
| ---            | ---       | ---       |
| `interface`    | yes       | no        |
| `class`        | yes       | yes       |
| `static class` | no        | no        |

#### Nullable types
- syntax: `type?`
- can contain a value + a `null`
- internally imlemented as a `struct Nullable<T>` that has `T Value` and `bool HasValue`

#### Pointers
- dangerous, won't be discussed too much in the first semester
- is never checked -- can be pointed **anywhere** (actually)
- isn't tracked by the garbage collector, so it can delete the instance without us knowing... the solution is **tracking references** (see `ref` section)

### Structures
- makes sense when we want the value semantics
	- `Vector`, `Color`, `Complex` structures, for example
- **no inheritance,** since the variable is always the value -- assigning would be broken
	- no `abstract`, no `virtual` methods
	- all user-defined structures are sealed
- as opposed to a class, a structure **always has a constructor without parameters** that is **empty**
	- even if we define some other one
	- we can't create one, since it's always there
	- we can't initialize values of variables before the constructor
	- done so we don't explicitly need to call a constructor

- if they're a part of a class/struct, the constructor is called automatically
- if they're on a stack, they can't be accessed until they are initialized

```cs
using System;

struct A {
    public int num;
    public int num2;
}

struct B {
    public static A a1;
    public A a2;
}

static class Program {
    static void Main(string[] args) {
        B b = new B();
        Console.WriteLine(B.a1.num);  // is ok
        Console.WriteLine(b.a2.num);  // is also ok

        A a;
        // Console.WriteLine(a.num);  // is not ok

        a.num = 5;
        Console.WriteLine(a.num);  // is ok

        // A a2 = a;  // is not ok, the entire struct has not been initialized

        a.num2 = 5;

        A a2 = a;  // is now ok
    }
}
```

- careful with putting them in `List<>` (or some other structure) and making them mutable -- if we attempt to do something like `myList[i].IncreaseByOne()`, it will just modify the returned copy and not do anything
	- this **doesn't happen with arrays**, since they're not using an indexer
	- it's generally a good idea to make structures immutable
	- `list[i].x = 1;` will break too (it uses the getter...)

### `readonly`
- used to set fields "read only" -- they can only be assigned in the constructor
- exceptions are caught during compilation
- can also be used in autoimplemented properties `int X { get; } = 5;`
	- this means that we can also assign to it in the constructor and only get it, so the effect is the same but it means something a little different
	- we could also just create a `readonly` field and a get-only property, but that's too much code

### Visibility
| Access Modifiers     | Meaning                                                           |
| ---                  | ---                                                               |
| `public`             | Access is not restricted.                                         |
| `private`            | Access is limited to the containing type.                         |
| `protected`          | Access is limited to the containing class derived types.          |
| `internal`           | Access is limited to the current assembly.                        |
| `protected internal` | Access is limited to the current assembly OR same/derived types.  |
| `private protected`  | Access is limited to the current assembly AND same/derived types. |

- by default:
	- visibility in **classes** is **private** (variables, methods...)
	- visibility in an **interface** is **public**
		- it doesn't make much sense to be private, since it's a public contract
- note that this works:

```cs
class A {
	private int x;
	
	// is OK
	public int GetX() {
		return x;
	}
	
	// is also OK, since this code is inside A
	public static void SetXOnB(B b) {
		b.x = 30;
	}
	
	public static int 
}
```

### `=>`
- syntactic sugar for:
	- when a non-`void` method returns something
	- when a void method has only one command
- also **works for getters and setters!**

### `??`, `??=`, `?.`
- conditional code execution, depending on whether something is `null` or not
- `a ?? b` returns `a`, if it isn't `null`, else `b`
- `x ??= y` will be assigned if `y` isn't `null`
- `x?.m()` will call the method if `x` isn't `null`
- `x?.f` will get the field value, if `x` isn't `null`

### `ref`
- call **by reference**
- address is passed and automatically de-referenced
- can point to heap/stack/static data
- parameter must be a variable, not an expression (like a number)
- makes sense if we really want to modify the passed variable

```cs
void Inc(ref int x) { x += 1; }

void f() {
	int val = 3;
	Inc(ref val);  // val will be 4
}
```

### `out`
- an alternative to `ref`
- useful for returning/setting multiple things in a function
- the CIL code is exactly the same, but the compiler checks, whether each `out` parameter has been assigned to (since the caller wouldn't know about the state of the variable)
	- we can't not assign the parameters (we have to at least assign dummy values)

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

- the variable can be declared as a part of the function call

```cs
int a;
if (tryParse(something, out a)) { Console.WriteLine("We failed: " + a); }
Console.WriteLine("We didn't fail: " + a);

// is the same as

if (tryParse(something, out int a)) { Console.WriteLine("We failed: " + a); }
Console.WriteLine("We didn't fail: " + a);
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
- not entirely an abstract class
	- classes/interface can implement multiple interfaces
	- classes can inherit only a single class
- note that each interface „inherits“ `System.Object`, since all objects inherit it too
	- not literally, it's #justcompilerthings

### Abstract classes
- sort of like interfaces, but with code
- we can define default members and methods that all classes inheriting this one will use

### Arithmetic overflows
```cs
checked {
	// kód
}
```
- is not controlled when functions are called from this block (how could it, when they're probably already translated...)

### `typeof(Class)`
- return the `Type` instance of the class
- useful when we're comparing types of variables

### `nameof(x)` [[Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/operators/nameof)]
- useful when debugging, when showing exceptions to users...
- better to do than `"x"`, since we can rename using any IDE easily

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

### Heaps and GC
- behavior of the garbage collector to the two heaps is different
- real limit is around {% latex %}1.4\ GB{% endlatex %} (for 32-bit systems)
	- `OutOfMemoryException` could happen sooner, since we could have a lot of holes in the given and the new object wouldn't fit in -- **heap fragmentation**
	- happens easily when resizing (dynamic array, for example), since we're creating a new array of twice the size, that has to co-exist with the old one for a bit
- **segment** -- reservation (virtual memory); around {% latex %}~16\ MB{% endlatex %}
	- varies greatly on the architecture and GC configuration!
- **kvantum** -- commit (physical memory); around {% latex %}~8\ kB{% endlatex %}
	- varies greatly on the architecture and GC configuration!
- GC is **generational**
	- gen 0 -- allocated here
	- gen 1 -- survives a GC
	- gen 2 -- survives another GC
	- GC of a given generation checks the generation and all above
	- the next generations are checked only if the previous ones didn't free too much memory
	- **ephemeral segment** -- the current newest segment of the garbage collector
		- this is where GC happens
		- once it is full, a new one is added and the old one becomes generation 2 segment
- `GC` -- a class for interacting with the GC:
	- checking the generation of the object
	- checking the number of generation collections
	- forcing a collection of a given generation
	- should be the **last resort**, since it usually does things well
- GC = no memory leaks is **not true** (or, well, to an extent...):
	- a global cache used in some classes doesn't get collected, since there is a reference to it

#### LOH (Large Object Heap)
- if it's larger than {% latex %}85\ 000\ B{% endlatex %}
- usually reached when the object contains an array
- no heap compacting (don't move objects when others die)

#### SOH (Small Object Heap)
- if it's smaller than {% latex %}85\ 000\ B{% endlatex %}

### Misc.

#### NuGet
- package manager

#### BenchmarkDotNet
- benchmarks

#### `prg.exe.config` (XML)
- configures .NET (garbage collection settings,...)
	- **server** mode doesn't do garbage collection as frequently, to be faster
	- **client** mode collects a lot (could be up to 30%)

