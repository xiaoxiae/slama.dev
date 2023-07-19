---
title: The C# programming language
category: "notes"
category_icon: /assets/category-icons/mff.webp
redirect_from:
- /lecture-notes/the-cs-programming-language/
excerpt: Lecture notes from The C# programming language lecture (Pavel Ježek, 2020/2021).
---

- .
{:toc}

{% lecture_notes_preface Pavel Ježek|2020/2021|en%}

Besides this, they have been slightly extended by some C#-specific questions for my [Bachelor's state exam](https://slama.dev/vzdelani/priprava-na-statnice-mff-uk/) that were not covered in the lecture, namely generics and functional elements.

### Strings
- internally an array of chars
- **immutable** (neither length nor contents)
	- concatenation creates new strings
		- `String.concat(s1, s2, s3, ...);` is good for concatenating a lot of them
			- `s = "a" + "bcd" + "ef";` internally uses this method, so it isn't slow
- `System.String` is the same as `string`
	- can't ever be a name of a variable!
	- removes the confusion -- what if someone decides to implement a `String` class
- `==` compares contents, char by char (same as `.Equals()`)
	- we can use `object.ReferenceEquals(o1, o2)` if we want reference equality

| Action                       | Code                                             |
| ---                          | ---                                              |
| split                        | `s.Split(char);`                                 |
| split on multiple delimiters | `s.Split(delimiters);`, `delimiters` is `char[]` |
| convert to integer           | `int.Parse(string);`, can throw!                 |
| length                       | `s.Length;`                                      |

#### Interning
- hashmap for reusing already created strings
- only for constants, not variables (only exception being `""`)!
- we can do this ourselves using `String.Intern(str);` -- if the table contains it, return it; else add it to the table
	- should be limited use: strings can't be removed from the table

#### `System.Text.StringBuilder`
- essentially a **mutable string**
- internally behaves like a dynamic array
	- quick operations like concatenation
- `.ToString()` returns a proper string (since we can't use `StringBuilder` anywhere we want a string)
	- no copying happens -- internally, the new string points to the contents of the `StringBuilder` (so we don't have to copy twice)
	- if we were to modify the string builder again, it gets copied

#### Interpolation
- `Console.Write("cislo = {0} a {1}", i, j");`
	- same as `Console.Write("cislo = " + i.ToString() + " a " + j.ToString())`,
	- calls `String.Format("format string", i, j)`
		- creates new string

```cs
Console.WriteLine("{0}: Hello, {1}!", s1, s2);

// careful, what if s2 == "{0}"
Console.WriteLine("{0}: Hello, " + s2 + "!", s1, s2);
```

- **interpolated strings** -- `$"My name is {name} and I'm {age}."`
	- is translated into a `String.Format` call (at compile time)... most of the time
	- if assigned to a `FormattableString`, its instance is created instead
		- `.GetArgument(i)` returns the i-th argument
		- `.Format()` creates a string
	- the `{}` blocks can be additionaly formatted using `:<format>` and `, <format>`

### Chars
- `System.Char` == `char` (keyword)
- 2-byte UTF-16 character
	- some characters must be at least a string, since some UTF-16 characters can be up to 4 bytes
- `\xABCD` -- unicode code in hex, consumes **one to four hex characters**
- `\uABCD` -- unicode code in hex, consumes **exactly four hex characters**
- `\UABCDEFGH` -- unicode code in hex, consumes **exactly eight hex characters**
	- note that while it does mean a single character, this has to be a string

### File I/O

- if we're dealing with binary I/O, use `FileStream` instead; this is for text

| Action     | Code                                                              |
| ---        | ---                                                               |
| reading    | `System.IO.StreamReader f = new System.IO.StreamReader(path);`    |
| read line  | `f.ReadLine();`                                                   |
| read chars | `int chars_read = f.Read(buffer, 0, BUFFER_SIZE);`                |
| writing    | `System.IO.StreamWriter f = new System.IO.StreamWriter(path);`    |
| write line | `f.WriteLine(line);`                                              |
| close      | `f.Dispose();`                                                    |

### Classes

#### Constructor
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
// note that stuff can be arbitrary code

class A {
	A () {
		int x = stuff;
	}
}
```

- everything in C# inherits `: object == System.Object` (if not inheriting anything)

When inheriting, the constructor of the predecessor is called like this:

```cs
class B : A {
	int x = stuff;
	
	B () {
		stuff2
	}
}

// is equivalent to (for each constructor!)
// note that stuff can be arbitrary code

class B : A {
	B () {
		int x = stuff;
		
		// constructor of A (without parameters)
		
		stuff2
	}
}
```

If no constructor without parameters exist (for example when a class contains one with parameters, which makes the one without parameters not generate) and we inherit the class without calling it, it won't compile:

```cs
// THIS WON'T COMPILE!

class A {
	public A(int x) { }
}

class B : A {
}
```

We have to do this instead:

```cs
class A : B {
	A () : base(/*parameters for constructor of B*/) {stuff}
}

// is equivalent to (for each constructor!)
// note that stuff can be arbitrary code

class A : B {
	A () {
		int x = something;
		
		// constructor of B (with the appropriate parameters)
		
		stuff
	}
}
```

- calling one constructor from another constructor:
	- `A(): this(constructor parameters) {}`
	- the stuff that would be called before `A()` isn't called (so we don't do it twice)

#### Static/class constructor
- same as a regular constructor but for static variables
- called before the first time an object of the class is instantiated
	- if no object is constructed, it is never called
	- if we do `Class a;`, then it's also not called!
- if none is specified, a default blank one is instantiated
	- this means that it can never have parameters
- internally called `.cctor`

```cs
class A {
	static A() { }
}
```

#### Destructors/finalizers
- same name as the class, but prepended with a tilde (`~`)
- has no return type and no parameters
- cannot be defined in structures
- called when the object is **destroyed** (by the GC)

#### Inheritance
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

##### Virtual/abstract/new methods
- it sometimes makes sense to implement a function differently in a child... **member hiding**
	- if we're looking at `B` like it's `A`, the `A` implementation would be called (if it's not virtual)
	- a warning is issued -- did we really want to do this?
		- what if we called the method from some other method in `A`?
		- we can use `new` to let it know that we really wanted to do this

```cs
class A {
	public virtual void f() { Console.WriteLine("A"); }
	public virtual void g() { Console.WriteLine("A"); }
}

class B : A {
	public override void f() { Console.WriteLine("B"); }
	
	// new is optinal, suppresses a warning
	public new void g() { Console.WriteLine("B"); }
}

(new B()).f();  // prints B
(new B()).g();  // prints B

((A)(new B())).f();  // prints B
((A)(new B())).g();  // prints A
```

```cs
class Animal {
	public virtual void Name() { Console.WriteLine("Animal"); }
}

class Mammal: Animal {
	public override void Name() { Console.WriteLine("Mammal"); }
}

class Dog: Mammal {
	// new is optinal, suppresses a warning
	public new virtual void Name() { Console.WriteLine("Dog"); }
}

class Beagle: Dog {
	public override void Name() { Console.WriteLine("Beagle"); }
}

Dog pet = new Beagle();
pet.Name();              // prints Beagle

Animal pet = new Beagle();
pet.Name();              // prints Mammal
```

- `new` **creates a new record,** `override` **overrides the current one:**
	- it doesn't matter that a method with the same name already existed

|          | `A` | `M` | `D` | `B` |
| ---      | --- | --- | --- | --- |
| `A.Name` | `A` | `M` | `M` | `M` |
| `D.Name` |     |     | `D` | `B` |

- if `abstract` is used, an entry in VTM is created but no implementation is provided
	- the entire class has to be `abstract` so it can't be instantiated, since the method has to be overriden
- virtual methods can be called from the constructor and act correctly, since `Type` (and its VMT) must have been initialized by then
- `virtual` is essentially a promise to the user that it's fine to provide an alternate implementation in the child without breaking the entire class
- `base` can be used to call a method from the parent non-virtually (even if it were)

##### Superclass to subclass conversion
- take `A` and `B` from the code above; `B b = (B)a;` has to be checked at runtime
	- the conversion is explicit, because it's something to think about
- if it's wrong `InvalidCastException` is thrown, so test the code!

###### `is`
- checks, whether `object` is of the given `Type` (or type of any of its children)
- runtime calls a method, not too quick of an operation -- has to go through the class tree!
- if `object` is `null`, `false` is always returned, though it seems that `null` can be anything

###### `as`
- returns the `object` if it is of the given `Type` (or type of any of its children), else `null`

```cs
B b = a as B;  // assigns `a` to `b` if it's of the valid type
               // this is the reason why `null is A` returns false

if (b != null) {
	// do stuff with `B b`
}

// is almost equivalent to (since C# 7.0)
// only difference is that `b` is not initialized after

if (a is B b) {
	// do stuff with `B b`
}
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
		- also contains a **virtual method table** (VMT)
	- `public virtual bool Equals(object o);`
		- for checking, whether two objects are equal
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
- prevents inheritance and allows for some code optimizations
	- no virtual function calls
- `sealed class A {}` -- is not inheritable
- `sealed override void m()` -- is not overridable

#### Generic classes
- useful when we have a lot of similar classes that differ by types
- can be used for `struct`s and `interface`s too

```
class FixedStack<T> {
	T[] a;
	int num;
	
	public FixedStack(int maxSize) {
		a = new T[maxSize];
	}
	
	public void push(T val) {
		a[num] = val;
		num += 1;
	}
	
	public T pop() {
		num -= 1;
		T ret = a[num];
		return ret;
	}
}
```

### Variable scope

#### Local variables
- created each time we enter `{`, deleted each time we leave `}`
	- but is still extremely fast and highly optimized by the compiler
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

### Exceptions
- all exceptions must inherit the `System.Exception` class
	- even the ones from other languages are wrapped in a `SEHException`
- takes a _long_ time (a lot of things have to be collected), though a `try` block is basically free
- watch out for exceptions that 
	1. can't be caught (like `StackOverflowException`)
	2. probably shouldn't be caught (like `OutOfMemoryException`)

#### `System.Exception`

| Property/Function | Meaning                             |
| ---               | ---                                 |
| `e.Message`       | `string` error message              |
| `e.StackTrace`    | `string` trace of method call stack |
| `e.Source`        | `string` app/object that threw it   |
| `e.ToString()`    | `string` the formatted exception    |

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

#### Common exception classes
- it's important to distinguish exceptions due to bugs (`NullReferenceException`, `IndexOutOfRangeException`) and due to incorrect program usage (possibly `FileNotFoundException` and many others)

---

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
```

- is also equivalent to (since C# 8.0, with `Dispose` being called when `x` goes out of scope)

```cs
using type x = new Type();
```

- only works with objects that inherit `IDisposable` \(\implies\) have a `Dispose` method

### Properties

```cs
T Property {
	get { /* stuff to do */ }
	set { /* stuff to do (with a variable `value`) */ }
}
```

- syntactic sugar for defining a `T get()` and `void set(T value)` methods
	- must be used with `=`, although it does generate methods `get_*` and `set_*` (so don't name other methods like that)
- is nice when we want to let the programmer know that we're just setting/getting something (although it may do something more complex)
	- it's generally a good idea to not make it too slow, since the syntax looks instant
-  when doing assemblies, properties make it so we don't need to rebuild code that uses it, since the API stays the same (which can be desirable)
- interfaces can also contain them (not the implementation, just that it has to have one)

#### Auto-implemented
- if we're just doing `get => value` and `set = value`, we can just do `get;` and `set;` and the code will get automatically generated
	- what if we want to make an interface out of it in the future?
	- what if we want to add constraints to the values in the future?
- we can also set default values: `int X { get; set; } = 12;`
- we can also explicitly set the accessibility of the functions: `public int Length { get; private set; }`
	- `public` affects `get`, since it doesn't have an explicit modifier, but not `set`, because it has one

#### Read-only
- `set` can be omitted, which makes the property read-only
- this means it can only be changed in the constructor and nowhere else

#### Instantiating objects with properties
```cs
A a = new A { x = 3; y = 6 };

// is literally the same as

A a = new A();
a.x = 3;
a.y = 6;
```

- this implies that the setter can't be `private`, since it's just syntactic sugar!

#### Parametric properties (indexers)
- for defining indexing on an object of the given class
- can be overloaded, since it's just a method (but might not be the smartest thing to do)
- are compiled into `get_Item` and `set_Item`

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

### Type System
- we can't choose whether something is a value or a reference -- it is determined by its type

#### Value types
- variable is always passed by **value** (assigning **copies it over**)
- usually allocated in-place on the **stack** (with exceptions, like when a part of a class)
- contains:
	- `struct`ures
	- simple types (`int`, `char`)
	- `Nullable`s (it's just a struct)
	- enumerations
	- is weird, since it's completely different to references that are allocated
- **can implement interfaces**, but boxing happens when we assign to `I var`
	- watch out for passing stuctures to function and doing something to them, since they will be boxed and nothing will change...

##### Simple types
- things like `byte`, `short`, `int`, `char`, `bool`...
- CLR and JIT knows about it, so operators (think `+`) is not a function call
- sizes are (almost) always defined (not like C++), except:
	- `nint` and `nuint` -- native, platform-dependent `(u)int` (since C# 9.0)
	- `bool` is only `true/false`, so it isn't defined too (implementation detail)
- `decimal` -- exponent is decimal, so numbers like `0.1` are precies
	- the downside is that it is much slower
- all of them are perpendicular to one another in the type hierarchy, but there **are conversions**
	- it is an actual conversion, not like for reference types (just checks in that case)
	- **implicit** conversions happen automatically, while **explicit** are manual
		- although a conversion is implicit, it can have data loss (`long` \(\rightarrow\) `float`)
	- they are **not free,** it can sometimes take quite a while (`int` \(\rightarrow\) `float`)
	- no conversions from/to `bool`

![Implicit Conversions.](/assets/the-cs-programming-language/implicit-conversions.svg)

- by default, all numeric constants (without a period) are `int`
	- however, we can do `long a = 10;`, it's optimized to not do a conversion
	- when a specific constant type is desired, we can use the following suffixes:
		- unsigned int/long: `u`
		- long, unsigned long: `l`
		- unsigned long: `ul`
- by default, all decimal number constants are `double`
	- we **can't do** `float f = 2.5;` (but must do `2.5f`)
	- other suffixes include
		- `d` for `double`
		- `m` for `decimal`
- when designing APIs, it might be a good idea to do `Int32` instead of `int`, so programmers from other languages now exactly what we mean

##### Nullable types
- `int? x` is a nullable variable -- can contain its value, or `null`
- internally imlemented as a `struct Nullable<T>` that has `T Value` and `bool HasValue` memobers
- `bool?`'s `null` value is "i don't know" so we can use `|` and `&` and get results we expect

#### Reference types
- variable is always passed by **reference** (assigning **creates a new reference to it**)
- the variable data is allocated and stored on managed **heaps**
- can only ever be assigned a reference to the heap
- can be `null`
	- actually, since C# 8.0, we can toggle this behavior and forbid it to contain a `null`
	- only gives warnings, since the compiler can't always determine that it's not from static analysis (although we can specify to treat certain warnings as errors)
- contains:
	- `class`es
	- `interface`s
	- arrays
	- delegates
- takes up more memory, since it has to contain:
	- the reference to the heap, where the value is
	- **heap overhead**
		1. which type it is (reference to an instance of the class `MethodTable`)
			- is either \(4/8B\), depending on the architecture
		2. syncblock -- related to threads and locking
			- always \(4B\)
		- padded to nearest \(8B\)

##### Arrays
- each new type inherits `System.Array` and is a new .NET type
- is sort of like generic types -- code is generated for each variant

| Action            | Code                                                |
| ---               | ---                                                 |
| create            | `int[] array = new int[size];`                      |
| create statically | `int[] array = {1, 2, 3};`                          |
| fill with stuff   | `Array.Fill(table, -1, 0, 256);`, requires `System` |
| sort              | `Array.Sort(array);`, highly optimized              |
| length            | `.Length`                                           |

- array of `struct` automatically calls constructors on them so we don't have to
- array of `class` is `null` by default
- **jagged** multidimensional arrays:
	- `int[][] a = new int[2][]`
	- can have different row lengths
	- takes a lot of memory (each row is a pointer) and is not generally nice to it
- **rectangular** multidimensional arrays:
	- single memory object
	- has to have same row lengths
	- nicer to memory
	- `int[,] a = new int[2, 3]`

#### (un)boxing
- crossing the bounday between a reference type and a value type
- `object o = 5;` creates a new object on the heap where the reference points to
- is immutable for simple value types, because... how would we modify it?

### Functional elements

#### Local functions
- a function defined locally
- can access parameters and local variables

```cs
static void Main(string[] args) {
	WriteLine("hello");
	
	double arg(int n) {
		return double.Parse(args[n]);
	}
	
	double d = arg(0);
	double e = arg(1);
	WriteLine(d + e);
}
```

#### Delegates
- value representing function or method
- defined using the `delegate` keyword

```cs
using System;

static class Program {
	public delegate bool Condition(int i);
	
	public static void TestNumbers(Condition condition) {
		for (int i = 0; i < 10; i++) {
			if (condition(i))
				Console.WriteLine(i);
		}
	}

	public bool IsEven(int i) => i % 2 == 0;
	public bool IsOdd(int i) => i % 2 == 1;

	static void Main(string[] args) {
		TestNumbers(IsEven);
	}
}
```

- they can also be generic: `delegate bool Condition<T>(T t)`

#### Lambda funtions
- functions defined using an expression: `parameters => expression`
- can be converted into a delegate -- `IsEven` above would be `i => i % 2 == 0`

### Structures
- only makes sense when we want the value semantics but more complex behavior
	- `Vector`, `Color`, `Complex` structures, for example
- **no inheritance,** since the variable is always the value -- assigning to variables would be broken (and is one of the main reasons for inheritance), which means:
	- no `abstract`, no `virtual` methods -- all user-defined structures are essentially sealed
- as opposed to a class, a structure **always has an empty constructor without parameters**
	- we **can't** define one, since it's always there
	- is preserved when we define another one
- if they're a part of a class/struct, the constructor is called automatically when initialized

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
        Console.WriteLine(a.num);  // is NOT OK
                                   // we haven't called the constructor

        a.num = 5;
        Console.WriteLine(a.num);  // is ok

        A a2 = a;  // is still NOT OK
                   // the entire struct must be initialized

        a.num2 = 5;

        A a3 = a;  // is ok
    }
}
```

- careful with putting them in `List<S>` (or some other structure) and making them mutable -- if we attempt to do something like `myList[i].IncreaseByOne()`, it will just modify the returned copy and not do anything
	- this **doesn't happen with arrays**, since they're not using an indexer
	- it's generally a good idea to make structures immutable, because users will use it like this

### Visibility

| Access Modifiers     | Access is...                                            |
| --:                  | ---                                                     |
| `public`             | not restricted.                                         |
| `private`            | limited to the containing type.                         |
| `protected`          | limited to the containing class derived types.          |
| `internal`           | limited to the current assembly.                        |
| `protected internal` | limited to the current assembly OR same/derived types.  |
| `private protected`  | limited to the current assembly AND same/derived types. |

- by default:
	- visibility of classes/interfaces/structs is `internal`
	- visibility in `class`es is `private`
	- visibility in `interface`s is `public`
		- it doesn't make much sense to be private, since it's a public contract

```cs
class A {
	private int x;
	
	// is ok, x is private in A
	public int GetX() {
		return x;
	}
	
	// is ALSO OK, since the code is inside A (B : A)
	public static void SetXOnB(B b) {
		b.x = 30;
	}
}
```

### `readonly`
- used to set fields **not assignable**, except in the **constructor**
- can also be used in autoimplemented properties (`int X { get; } = 5;`)

### `=>`
- syntactic sugar for:
	- when a non-`void` method returns something
	- when a void method has only one command

### `??`, `??=`, `?.`
- conditional code execution, depending on whether something is `null` or not
- `a ?? b` returns `a`, if it isn't `null`, else `b`
- `x ??= y` will be assigned if `y` isn't `null`
- `x?.m()` will call the method if `x` isn't `null`
- `x?.f` will get the field value, if `x` isn't `null`

#### Arithmetic overflows
```cs
checked {
	// kód
}
```
- is not controlled when functions are called from this block (how could it, when they're probably already translated...)

### References

#### `ref`
- a **tracking reference**
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

- calling a method on an object is just a shortcut for doing `Class.function(ref this, <other parameters>)`

#### `out`
- an alternative to `ref`
- useful for returning/setting multiple things in a function
- the CIL code is exactly the same, but the compiler checks, whether each `out` parameter has been assigned to (since the caller wouldn't know about the state of the variable)
	- we must assign the parameters (at least dummy values)

```cs
void Read(out int first, out int next) {
	first = Console.Read();
	next = Console.Read();
}

void Main() {
	int first, next;
	Read(out first, out next);
}
```

- the variable can be declared as a part of the function call

```cs
int a;
if (tryParse(something, out a))
	Console.WriteLine("We failed: " + a);

Console.WriteLine("We didn't fail: " + a);

// is the same as

if (tryParse(something, out int a))
	Console.WriteLine("We failed: " + a);

Console.WriteLine("We didn't fail: " + a);
```

### `var`
- derived at compile time, depending on what is on the right side
- if we can't determine the type, the code won't compile
	- `var x;`
	- `var y = (1, 2, 3);`
	- `var z = null`
- the declaration is a comment -- it's unwise to write `var` everywhere:
	- `var name = GetName();` -- what does it return?
	- `var d = new List<int>();` --  what if I want to change List to a HashSet later (and interface would thus be better to use)?

### Interfaces
- a **contract** -- we can assign any `class` that implements an interface to variables with an interface (when we only require the functionality of the given interface)
	- we can do the same for a `struct`, but it involves boxing

```cs
interface Shape {
	double Perimeter();
	double Area();
}
```

- **can't be instantiated** (it has no code)
- not entirely an abstract class
	- classes/interface can implement multiple interfaces
	- classes can inherit only a single class
	- interfaces can't have code, abstract classes can

### Implementation details

#### Heaps and garbage collection
- **two heaps**; behavior of the garbage collector to the two heaps is different
- real limit is around \(1.4\ GB\) (for 32-bit systems)
	- `OutOfMemoryException` could happen sooner, since we could have a lot of holes in the given heap and the new object wouldn't fit in -- **heap fragmentation**
	- happens easily when resizing (dynamic array, for example), since we're creating a new array of twice the size, that has to co-exist with the old one for a bit
- **segment** -- reservation (virtual memory); around \(~16\ MB\)
	- varies greatly on the architecture and GC configuration!
- **kvantum** -- commit (physical memory); around \(~8\ kB\)
	- varies greatly on the architecture and GC configuration!
- GC is **generational**
	- gen 0 -- allocated just now
	- gen \(n\) -- survived \(n\) garbage collections
	- GC of a given generation checks the generation and all above
	- the next generations are checked only if the previous ones didn't free too much memory
	- **ephemeral segment** -- the current newest segment of the garbage collector
		- this is where GC happens
		- once it is full, a new one is added and the old one becomes generation 2 segment
- `GC` class -- for interacting with the GC:
	- checking the generation of the object
	- checking the number of generation collections
	- forcing a collection of a given generation
	- should be the **last resort**, since it usually does things well
- GC \(\implies\) no memory leaks is **not true** (to an extent...):
	- when a global cache used in classes doesn't get collected
	- when objects subscribe to events and don't unsubscribe
	- when an anonymous method references an attribute from an object

##### Large Object Heap (LOH)
- if it's larger than \(85\ 000\ B\)
- usually reached when the object contains an array
- no heap compacting (don't move objects when others die)

##### Small Object Heap (SOH)
- if it's smaller than \(85\ 000\ B\)
- yes heap compacting (move after the end of garbage collection)

### Terms to know

#### CIL
- **common intermediate language**
- formerly known Microsoft Intermediate Language (MSIL) or Intermediate Language (IL)
- intermediate language binary instruction set for the CLI specification
- executed by CLI-compatible runtime like **CLR**
- object-oriented, stack-based, typically JITted into native code

#### CLR
- run-time environment for the .NET framework
- responsible for running .NET programs, regardless of the language
- contains things like **GC** and **JIT compiler**

#### GAC
- **global assembly cache** -- stores assemblies to be shared by computer applications

#### JIT
- **just in time** -- when it's needed
- the default unit is **1 method**
- function calls are translated to calls to **stubs**
	- short calls that call JIT and fix references to the method in the code
- compilation is spaced into the running time of the program
	- can mess benchmarks up -- make sure we're testing when the method has already been JITted
- also **takes care of optimizations,** since optimizing CIL code doesn't make much sense
	- means that they can't be overly aggressive
- does **method inlining** (moves body of the method to where it's called)
	- can't always be done (recursive functions)
	- generally happens for smaller (\(<32\ B\) of machine code) methods that aren't too complicated (no `try/catch`, for example)

#### AOT
- **ahead-of-time** -- before it's needed
- `ngen.exe` -- pre-JITting code
- more intensive optimizations
- JITting can still happen when it's needed, though
- will be an important feature in .NET 5

#### BCL
- **base class library**
- types for built-in CLI data types, basic file access, collections, formatting,...

#### .NET
- **BCL + CLR**

#### Tiered compilation
- multiple compilations of the same method that can be swapped
	- initially quickly JITted but kinda slow
	- JITted properly after a number of calls to the method

#### CLS
- common language specification
- what a language must do in order to be .NET-compliant
- specifies things like minimum types:
	- `sbyte`, `ushort` are not compliant, so making them parameters of a function called from some other DLL might not be the best idea; on the other hand, implementation details are quite fine

#### `typeof(Class)`
- return the `Type` instance of the class
- useful when we're comparing types of variables

#### `nameof(x)` [[Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/operators/nameof)]
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

#### NUnit tests

```cs
using System;
using NUnit.Framework;

public class Tests
{
	[SetUp]
	public void Setup() { /* do something for setup (optional) */ }
	
	[Test]
	public void NameOfTheTest()
	{
		Assert.AreEqual("a", "a");
		Assert.AreNotEqual("a", "b");
		Assert.IsTrue(true);
		Assert.IsFalse(false);
		
		Assert.Throws<ArgumentException>(() =>
		{
			This doesn't throw!
		});
	}
}
```

### Data structures

#### Dictionaries
- `using System.Collections.Generic;`

| Action   | Code                                                   |
| ---      | ---                                                    |
| create   | `Dictionary<int, int> d = new Dictionary<int, int>();` |
| contains | `d.ContainsKey(element);`                              |
| add      | `d[index] = element;`                                  |

#### Queues

| Action | Code                                         |
| ---    | ---                                          |
| create | `Queue<string> q = new Queue<string>();`     |
| add    | `q.Enqueue(element);`                        |
| pop    | `q.Dequeue(element);`                        |
| size   | `q.Count;`                                   |
| peek   | `q.Peek();`                                  |

### Acknowledgements
- Adam Dingle, whose [Programming 2 notes](/assets/priprava-na-statnice-mff-uk/prog2.pdf) I've shamelessly copied (for certain examples)
