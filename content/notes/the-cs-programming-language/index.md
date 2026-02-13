---
date: '2021-02-19'
title: The C# programming language
description: Lecture notes from The C# programming language lecture (Pavel Ježek,
  2020/2021).
categoryIcon: /assets/category-icons/mff.webp
toc: true
---

{{< lecture_notes_preface "Pavel Ježek | 2020/2021 | MFF" >}}

Besides this, they have been slightly extended by some C#-specific questions for my [Bachelor's state exam](https://slama.dev/vzdelani/priprava-na-statnice-mff-uk/) that were not covered in the lecture, namely generics and functional elements.

### Strings
- internally an array of chars
- **immutable** (neither length nor contents)
	- concatenation creates new strings
		- {{< inline_highlight "cs" >}}String.concat(s1, s2, s3, ...);{{< /inline_highlight >}} is good for concatenating a lot of them
			- {{< inline_highlight "cs" >}}s = "a" + "bcd" + "ef";{{< /inline_highlight >}} internally uses this method, so it isn't slow
- {{< inline_highlight "cs" >}}System.String{{< /inline_highlight >}} is the same as {{< inline_highlight "cs" >}}string{{< /inline_highlight >}}
	- can't ever be a name of a variable!
	- removes the confusion -- what if someone decides to implement a {{< inline_highlight "cs" >}}String{{< /inline_highlight >}} class
- {{< inline_highlight "cs" >}}=={{< /inline_highlight >}} compares contents, char by char (same as {{< inline_highlight "cs" >}}.Equals(){{< /inline_highlight >}})
	- we can use {{< inline_highlight "cs" >}}object.ReferenceEquals(o1, o2){{< /inline_highlight >}} if we want reference equality

| Action                       | Code                                             |
| ---                          | ---                                              |
| split                        | {{< inline_highlight "cs" >}}s.Split(char);{{< /inline_highlight >}}                                 |
| split on multiple delimiters | {{< inline_highlight "cs" >}}s.Split(delimiters);{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}delimiters{{< /inline_highlight >}} is {{< inline_highlight "cs" >}}char[]{{< /inline_highlight >}} |
| convert to integer           | {{< inline_highlight "cs" >}}int.Parse(string);{{< /inline_highlight >}}, can throw!                 |
| length                       | {{< inline_highlight "cs" >}}s.Length;{{< /inline_highlight >}}                                      |

#### Interning
- hashmap for reusing already created strings
- only for constants, not variables (only exception being {{< inline_highlight "cs" >}}""{{< /inline_highlight >}})!
- we can do this ourselves using {{< inline_highlight "cs" >}}String.Intern(str);{{< /inline_highlight >}} -- if the table contains it, return it; else add it to the table
	- should be limited use: strings can't be removed from the table

#### {{% inline_highlight "cs" %}}System.Text.StringBuilder{{% /inline_highlight %}}
- essentially a **mutable string**
- internally behaves like a dynamic array
	- quick operations like concatenation
- {{< inline_highlight "cs" >}}.ToString(){{< /inline_highlight >}} returns a proper string (since we can't use {{< inline_highlight "cs" >}}StringBuilder{{< /inline_highlight >}} anywhere we want a string)
	- no copying happens -- internally, the new string points to the contents of the {{< inline_highlight "cs" >}}StringBuilder{{< /inline_highlight >}} (so we don't have to copy twice)
	- if we were to modify the string builder again, it gets copied

#### Interpolation
- {{< inline_highlight "cs" >}}Console.Write("cislo = {0} a {1}", i, j");{{< /inline_highlight >}}
	- same as {{< inline_highlight "cs" >}}Console.Write("cislo = " + i.ToString() + " a " + j.ToString()){{< /inline_highlight >}},
	- calls {{< inline_highlight "cs" >}}String.Format("format string", i, j){{< /inline_highlight >}}
		- creates new string

```cs
Console.WriteLine("{0}: Hello, {1}!", s1, s2);

// careful, what if s2 == "{0}"
Console.WriteLine("{0}: Hello, " + s2 + "!", s1, s2);
```

- **interpolated strings** -- {{< inline_highlight "cs" >}}$"My name is {name} and I'm {age}."{{< /inline_highlight >}}
	- is translated into a {{< inline_highlight "cs" >}}String.Format{{< /inline_highlight >}} call (at compile time)... most of the time
	- if assigned to a {{< inline_highlight "cs" >}}FormattableString{{< /inline_highlight >}}, its instance is created instead
		- {{< inline_highlight "cs" >}}.GetArgument(i){{< /inline_highlight >}} returns the i-th argument
		- {{< inline_highlight "cs" >}}.Format(){{< /inline_highlight >}} creates a string
	- the {{< inline_highlight "cs" >}}{}{{< /inline_highlight >}} blocks can be additionaly formatted using {{< inline_highlight "cs" >}}:<format>{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}, <format>{{< /inline_highlight >}}

### Chars
- {{< inline_highlight "cs" >}}System.Char{{< /inline_highlight >}} == {{< inline_highlight "cs" >}}char{{< /inline_highlight >}} (keyword)
- 2-byte UTF-16 character
	- some characters must be at least a string, since some UTF-16 characters can be up to 4 bytes
- {{< inline_highlight "cs" >}}\xABCD{{< /inline_highlight >}} -- unicode code in hex, consumes **one to four hex characters**
- {{< inline_highlight "cs" >}}\uABCD{{< /inline_highlight >}} -- unicode code in hex, consumes **exactly four hex characters**
- {{< inline_highlight "cs" >}}\UABCDEFGH{{< /inline_highlight >}} -- unicode code in hex, consumes **exactly eight hex characters**
	- note that while it does mean a single character, this has to be a string

### File I/O

- if we're dealing with binary I/O, use {{< inline_highlight "cs" >}}FileStream{{< /inline_highlight >}} instead; this is for text

| Action     | Code                                                              |
| ---        | ---                                                               |
| reading    | {{< inline_highlight "cs" >}}System.IO.StreamReader f = new System.IO.StreamReader(path);{{< /inline_highlight >}}    |
| read line  | {{< inline_highlight "cs" >}}f.ReadLine();{{< /inline_highlight >}}                                                   |
| read chars | {{< inline_highlight "cs" >}}int chars_read = f.Read(buffer, 0, BUFFER_SIZE);{{< /inline_highlight >}}                |
| writing    | {{< inline_highlight "cs" >}}System.IO.StreamWriter f = new System.IO.StreamWriter(path);{{< /inline_highlight >}}    |
| write line | {{< inline_highlight "cs" >}}f.WriteLine(line);{{< /inline_highlight >}}                                              |
| close      | {{< inline_highlight "cs" >}}f.Dispose();{{< /inline_highlight >}}                                                    |

### Classes

#### Constructor
- same syntax as C++, but it's a good idea to add a {{< inline_highlight "cs" >}}public{{< /inline_highlight >}} before it
- if none is specified, a default one without parameters is created
	- note that we have to write it explicitly if we want it besides one with parameters!
- translated to a {{< inline_highlight "cs" >}}.ctor{{< /inline_highlight >}} method (see disassembly)
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

- everything in C# inherits {{< inline_highlight "cs" >}}: object == System.Object{{< /inline_highlight >}} (if not inheriting anything)

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
	- {{< inline_highlight "cs" >}}A(): this(constructor parameters) {}{{< /inline_highlight >}}
	- the stuff that would be called before {{< inline_highlight "cs" >}}A(){{< /inline_highlight >}} isn't called (so we don't do it twice)

#### Static/class constructor
- same as a regular constructor but for static variables
- called before the first time an object of the class is instantiated
	- if no object is constructed, it is never called
	- if we do {{< inline_highlight "cs" >}}Class a;{{< /inline_highlight >}}, then it's also not called!
- if none is specified, a default blank one is instantiated
	- this means that it can never have parameters
- internally called {{< inline_highlight "cs" >}}.cctor{{< /inline_highlight >}}

```cs
class A {
	static A() { }
}
```

#### Destructors/finalizers
- same name as the class, but prepended with a tilde ({{< inline_highlight "cs" >}}~{{< /inline_highlight >}})
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
	- if none is specified, {{< inline_highlight "cs" >}}System.Object == object{{< /inline_highlight >}} is used automatically

##### Virtual/abstract/new methods
- it sometimes makes sense to implement a function differently in a child... **member hiding**
	- if we're looking at {{< inline_highlight "cs" >}}B{{< /inline_highlight >}} like it's {{< inline_highlight "cs" >}}A{{< /inline_highlight >}}, the {{< inline_highlight "cs" >}}A{{< /inline_highlight >}} implementation would be called (if it's not virtual)
	- a warning is issued -- did we really want to do this?
		- what if we called the method from some other method in {{< inline_highlight "cs" >}}A{{< /inline_highlight >}}?
		- we can use {{< inline_highlight "cs" >}}new{{< /inline_highlight >}} to let it know that we really wanted to do this

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

- {{< inline_highlight "cs" >}}new{{< /inline_highlight >}} **creates a new record,** {{< inline_highlight "cs" >}}override{{< /inline_highlight >}} **overrides the current one:**
	- it doesn't matter that a method with the same name already existed

|          | {{< inline_highlight "cs" >}}A{{< /inline_highlight >}} | {{< inline_highlight "cs" >}}M{{< /inline_highlight >}} | {{< inline_highlight "cs" >}}D{{< /inline_highlight >}} | {{< inline_highlight "cs" >}}B{{< /inline_highlight >}} |
| ---      | --- | --- | --- | --- |
| {{< inline_highlight "cs" >}}A.Name{{< /inline_highlight >}} | {{< inline_highlight "cs" >}}A{{< /inline_highlight >}} | {{< inline_highlight "cs" >}}M{{< /inline_highlight >}} | {{< inline_highlight "cs" >}}M{{< /inline_highlight >}} | {{< inline_highlight "cs" >}}M{{< /inline_highlight >}} |
| {{< inline_highlight "cs" >}}D.Name{{< /inline_highlight >}} |     |     | {{< inline_highlight "cs" >}}D{{< /inline_highlight >}} | {{< inline_highlight "cs" >}}B{{< /inline_highlight >}} |

- if {{< inline_highlight "cs" >}}abstract{{< /inline_highlight >}} is used, an entry in VTM is created but no implementation is provided
	- the entire class has to be {{< inline_highlight "cs" >}}abstract{{< /inline_highlight >}} so it can't be instantiated, since the method has to be overriden
- virtual methods can be called from the constructor and act correctly, since {{< inline_highlight "cs" >}}Type{{< /inline_highlight >}} (and its VMT) must have been initialized by then
- {{< inline_highlight "cs" >}}virtual{{< /inline_highlight >}} is essentially a promise to the user that it's fine to provide an alternate implementation in the child without breaking the entire class
- {{< inline_highlight "cs" >}}base{{< /inline_highlight >}} can be used to call a method from the parent non-virtually (even if it were)

##### Superclass to subclass conversion
- take {{< inline_highlight "cs" >}}A{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}B{{< /inline_highlight >}} from the code above; {{< inline_highlight "cs" >}}B b = (B)a;{{< /inline_highlight >}} has to be checked at runtime
	- the conversion is explicit, because it's something to think about
- if it's wrong {{< inline_highlight "cs" >}}InvalidCastException{{< /inline_highlight >}} is thrown, so test the code!

###### {{% inline_highlight "cs" %}}is{{% /inline_highlight %}}
- checks, whether {{< inline_highlight "cs" >}}object{{< /inline_highlight >}} is of the given {{< inline_highlight "cs" >}}Type{{< /inline_highlight >}} (or type of any of its children)
- runtime calls a method, not too quick of an operation -- has to go through the class tree!
- if {{< inline_highlight "cs" >}}object{{< /inline_highlight >}} is {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}false{{< /inline_highlight >}} is always returned, though it seems that {{< inline_highlight "cs" >}}null{{< /inline_highlight >}} can be anything

###### {{% inline_highlight "cs" %}}as{{% /inline_highlight %}}
- returns the {{< inline_highlight "cs" >}}object{{< /inline_highlight >}} if it is of the given {{< inline_highlight "cs" >}}Type{{< /inline_highlight >}} (or type of any of its children), else {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}

```cs
B b = a as B;  // assigns {{< inline_highlight "cs" >}}a{{< /inline_highlight >}} to {{< inline_highlight "cs" >}}b{{< /inline_highlight >}} if it's of the valid type
               // this is the reason why {{< inline_highlight "cs" >}}null is A{{< /inline_highlight >}} returns false

if (b != null) {
	// do stuff with {{< inline_highlight "cs" >}}B b{{< /inline_highlight >}}
}

// is almost equivalent to (since C# 7.0)
// only difference is that {{< inline_highlight "cs" >}}b{{< /inline_highlight >}} is not initialized after

if (a is B b) {
	// do stuff with {{< inline_highlight "cs" >}}B b{{< /inline_highlight >}}
}
```

##### {{% inline_highlight "cs" %}}System.Object{{% /inline_highlight %}}
- inherited by all classes
- has the following members:
	- {{< inline_highlight "cs" >}}protected object MemberwiseClone();{{< /inline_highlight >}}
		- creates a shallow copy of the object (byte by byte)
		- doesn't make much sense for reference types
		- note that it is protected!
			- implement {{< inline_highlight "cs" >}}public A Clone() {...}{{< /inline_highlight >}} to make it public
			- there is an {{< inline_highlight "cs" >}}IClonable{{< /inline_highlight >}} interface, but it was before {{< inline_highlight "cs" >}}<T>{{< /inline_highlight >}}...
	- {{< inline_highlight "cs" >}}public Type GetType();{{< /inline_highlight >}}
		- done for all types ({{< inline_highlight "cs" >}}new Type("A"){{< /inline_highlight >}},...)
		- contains {{< inline_highlight "cs" >}}.Name{{< /inline_highlight >}} and other stuff for reflection
		- also contains a **virtual method table** (VMT)
	- {{< inline_highlight "cs" >}}public virtual bool Equals(object o);{{< /inline_highlight >}}
		- for checking, whether two objects are equal
	- {{< inline_highlight "cs" >}}public virtual string ToString();{{< /inline_highlight >}}
		- the string representation of the object
		- shouldn't be something too complicated (like a giant recursive function)
	- {{< inline_highlight "cs" >}}public virtual int GetHashCode();{{< /inline_highlight >}}
		- hash code of the object; for hashmap-like data structures
	- {{< inline_highlight "cs" >}}public static bool ReferenceEquals(object objA, object objB);{{< /inline_highlight >}}
		- whether the two objects are equal by reference

##### {{% inline_highlight "cs" %}}System.ValueType{{% /inline_highlight %}}
- is inherited by all types ({{< inline_highlight "cs" >}}int{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}Nullable{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}bool{{< /inline_highlight >}}, user-defined structures...)
- overrides {{< inline_highlight "cs" >}}Equals{{< /inline_highlight >}} to be byte-equal (since it is a value type)
	- if it has reference members, **uses reflection to check their values too** -- string, for example
		- better to implement it ourselves in this case

##### {{% inline_highlight "cs" %}}sealed{{% /inline_highlight %}}
- prevents inheritance and allows for some code optimizations
	- no virtual function calls
- {{< inline_highlight "cs" >}}sealed class A {}{{< /inline_highlight >}} -- is not inheritable
- {{< inline_highlight "cs" >}}sealed override void m(){{< /inline_highlight >}} -- is not overridable

#### Generic classes
- useful when we have a lot of similar classes that differ by types
- can be used for {{< inline_highlight "cs" >}}struct{{< /inline_highlight >}}s and {{< inline_highlight "cs" >}}interface{{< /inline_highlight >}}s too

```cs
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
- all exceptions must inherit the {{< inline_highlight "cs" >}}System.Exception{{< /inline_highlight >}} class
	- even the ones from other languages are wrapped in a {{< inline_highlight "cs" >}}SEHException{{< /inline_highlight >}}
- takes a _long_ time (a lot of things have to be collected), though a {{< inline_highlight "cs" >}}try{{< /inline_highlight >}} block is basically free
- watch out for exceptions that
	1. can't be caught (like {{< inline_highlight "cs" >}}StackOverflowException{{< /inline_highlight >}})
	2. probably shouldn't be caught (like {{< inline_highlight "cs" >}}OutOfMemoryException{{< /inline_highlight >}})

#### {{% inline_highlight "cs" %}}System.Exception{{% /inline_highlight %}}

| Property/Function | Meaning                             |
| ---               | ---                                 |
| {{< inline_highlight "cs" >}}e.Message{{< /inline_highlight >}}       | {{< inline_highlight "cs" >}}string{{< /inline_highlight >}} error message              |
| {{< inline_highlight "cs" >}}e.StackTrace{{< /inline_highlight >}}    | {{< inline_highlight "cs" >}}string{{< /inline_highlight >}} trace of method call stack |
| {{< inline_highlight "cs" >}}e.Source{{< /inline_highlight >}}        | {{< inline_highlight "cs" >}}string{{< /inline_highlight >}} app/object that threw it   |
| {{< inline_highlight "cs" >}}e.ToString(){{< /inline_highlight >}}    | {{< inline_highlight "cs" >}}string{{< /inline_highlight >}} the formatted exception    |

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
- it's important to distinguish exceptions due to bugs ({{< inline_highlight "cs" >}}NullReferenceException{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}IndexOutOfRangeException{{< /inline_highlight >}}) and due to incorrect program usage (possibly {{< inline_highlight "cs" >}}FileNotFoundException{{< /inline_highlight >}} and many others)

---

- {{< inline_highlight "cs" >}}Exception{{< /inline_highlight >}}
	- {{< inline_highlight "cs" >}}SystemException{{< /inline_highlight >}}
		- {{< inline_highlight "cs" >}}ArithmeticException{{< /inline_highlight >}}
			- {{< inline_highlight "cs" >}}DivideByZeroException{{< /inline_highlight >}}
			- {{< inline_highlight "cs" >}}OverflowException{{< /inline_highlight >}}
			- ....
		- {{< inline_highlight "cs" >}}NullReferenceException{{< /inline_highlight >}}
		- {{< inline_highlight "cs" >}}IndexOutOfRangeException{{< /inline_highlight >}}
		- {{< inline_highlight "cs" >}}InvalidCastException{{< /inline_highlight >}}
		- ...
	- {{< inline_highlight "cs" >}}ApplicationException{{< /inline_highlight >}}
		- user-defined exceptions
		- ...
	- {{< inline_highlight "cs" >}}IOException{{< /inline_highlight >}}
		- {{< inline_highlight "cs" >}}FileNotFoundException{{< /inline_highlight >}}
		- {{< inline_highlight "cs" >}}DirectoryNotFoundException{{< /inline_highlight >}}
		- ...
	- {{< inline_highlight "cs" >}}WebException{{< /inline_highlight >}}
	- ...


<!-- NOTE: using Go here because Chroma's C# lexer has a bug with "using" in inline highlights -->
### {{% inline_highlight "go" %}}using{{% /inline_highlight %}}

```cs
Type x;
try {
	x = new Type();  // could raise an exception!

	// some code
} finally {
	if (x != null) x.Dispose();
}
```
- is (sort of, because {{< inline_highlight "cs" >}}x{{< /inline_highlight >}} has a slightly different scope) equivalent to

```cs
using (type x = new Type()) {
	// some code
}
```

- is also equivalent to (since C# 8.0, with {{< inline_highlight "cs" >}}Dispose{{< /inline_highlight >}} being called when {{< inline_highlight "cs" >}}x{{< /inline_highlight >}} goes out of scope)

```cs
using type x = new Type();
```

- only works with objects that inherit {{< inline_highlight "cs" >}}IDisposable{{< /inline_highlight >}} \(\implies\) have a {{< inline_highlight "cs" >}}Dispose{{< /inline_highlight >}} method

### Properties

```cs
T Property {
	get { /* stuff to do */ }
	set { /* stuff to do (with a variable {{< inline_highlight "cs" >}}value{{< /inline_highlight >}}) */ }
}
```

- syntactic sugar for defining a {{< inline_highlight "cs" >}}T get(){{< /inline_highlight >}} and {{< inline_highlight "cs" >}}void set(T value){{< /inline_highlight >}} methods
	- must be used with {{< inline_highlight "cs" >}}={{< /inline_highlight >}}, although it does generate methods {{< inline_highlight "cs" >}}get_*{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}set_*{{< /inline_highlight >}} (so don't name other methods like that)
- is nice when we want to let the programmer know that we're just setting/getting something (although it may do something more complex)
	- it's generally a good idea to not make it too slow, since the syntax looks instant
-  when doing assemblies, properties make it so we don't need to rebuild code that uses it, since the API stays the same (which can be desirable)
- interfaces can also contain them (not the implementation, just that it has to have one)

#### Auto-implemented
- if we're just doing {{< inline_highlight "cs" >}}get => value{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}set = value{{< /inline_highlight >}}, we can just do {{< inline_highlight "cs" >}}get;{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}set;{{< /inline_highlight >}} and the code will get automatically generated
	- what if we want to make an interface out of it in the future?
	- what if we want to add constraints to the values in the future?
- we can also set default values: {{< inline_highlight "cs" >}}int X { get; set; } = 12;{{< /inline_highlight >}}
- we can also explicitly set the accessibility of the functions: {{< inline_highlight "cs" >}}public int Length { get; private set; }{{< /inline_highlight >}}
	- {{< inline_highlight "cs" >}}public{{< /inline_highlight >}} affects {{< inline_highlight "cs" >}}get{{< /inline_highlight >}}, since it doesn't have an explicit modifier, but not {{< inline_highlight "cs" >}}set{{< /inline_highlight >}}, because it has one

#### Read-only
- {{< inline_highlight "cs" >}}set{{< /inline_highlight >}} can be omitted, which makes the property read-only
- this means it can only be changed in the constructor and nowhere else

#### Instantiating objects with properties
```cs
A a = new A { x = 3; y = 6 };

// is literally the same as

A a = new A();
a.x = 3;
a.y = 6;
```

- this implies that the setter can't be {{< inline_highlight "cs" >}}private{{< /inline_highlight >}}, since it's just syntactic sugar!

#### Parametric properties (indexers)
- for defining indexing on an object of the given class
- can be overloaded, since it's just a method (but might not be the smartest thing to do)
- are compiled into {{< inline_highlight "cs" >}}get_Item{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}set_Item{{< /inline_highlight >}}

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
	- {{< inline_highlight "cs" >}}struct{{< /inline_highlight >}}ures
	- simple types ({{< inline_highlight "cs" >}}int{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}char{{< /inline_highlight >}})
	- {{< inline_highlight "cs" >}}Nullable{{< /inline_highlight >}}s (it's just a struct)
	- enumerations
	- is weird, since it's completely different to references that are allocated
- **can implement interfaces**, but boxing happens when we assign to {{< inline_highlight "cs" >}}I var{{< /inline_highlight >}}
	- watch out for passing stuctures to function and doing something to them, since they will be boxed and nothing will change...

##### Simple types
- things like {{< inline_highlight "cs" >}}byte{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}short{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}int{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}char{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}bool{{< /inline_highlight >}}...
- CLR and JIT knows about it, so operators (think {{< inline_highlight "cs" >}}+{{< /inline_highlight >}}) is not a function call
- sizes are (almost) always defined (not like C++), except:
	- {{< inline_highlight "cs" >}}nint{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}nuint{{< /inline_highlight >}} -- native, platform-dependent {{< inline_highlight "cs" >}}(u)int{{< /inline_highlight >}} (since C# 9.0)
	- {{< inline_highlight "cs" >}}bool{{< /inline_highlight >}} is only {{< inline_highlight "cs" >}}true/false{{< /inline_highlight >}}, so it isn't defined too (implementation detail)
- {{< inline_highlight "cs" >}}decimal{{< /inline_highlight >}} -- exponent is decimal, so numbers like {{< inline_highlight "cs" >}}0.1{{< /inline_highlight >}} are precies
	- the downside is that it is much slower
- all of them are perpendicular to one another in the type hierarchy, but there **are conversions**
	- it is an actual conversion, not like for reference types (just checks in that case)
	- **implicit** conversions happen automatically, while **explicit** are manual
		- although a conversion is implicit, it can have data loss ({{< inline_highlight "cs" >}}long{{< /inline_highlight >}} \(\rightarrow\) {{< inline_highlight "cs" >}}float{{< /inline_highlight >}})
	- they are **not free,** it can sometimes take quite a while ({{< inline_highlight "cs" >}}int{{< /inline_highlight >}} \(\rightarrow\) {{< inline_highlight "cs" >}}float{{< /inline_highlight >}})
	- no conversions from/to {{< inline_highlight "cs" >}}bool{{< /inline_highlight >}}

![Implicit Conversions.](implicit-conversions.svg)

- by default, all numeric constants (without a period) are {{< inline_highlight "cs" >}}int{{< /inline_highlight >}}
	- however, we can do {{< inline_highlight "cs" >}}long a = 10;{{< /inline_highlight >}}, it's optimized to not do a conversion
	- when a specific constant type is desired, we can use the following suffixes:
		- unsigned int/long: {{< inline_highlight "cs" >}}u{{< /inline_highlight >}}
		- long, unsigned long: {{< inline_highlight "cs" >}}l{{< /inline_highlight >}}
		- unsigned long: {{< inline_highlight "cs" >}}ul{{< /inline_highlight >}}
- by default, all decimal number constants are {{< inline_highlight "cs" >}}double{{< /inline_highlight >}}
	- we **can't do** {{< inline_highlight "cs" >}}float f = 2.5;{{< /inline_highlight >}} (but must do {{< inline_highlight "cs" >}}2.5f{{< /inline_highlight >}})
	- other suffixes include
		- {{< inline_highlight "cs" >}}d{{< /inline_highlight >}} for {{< inline_highlight "cs" >}}double{{< /inline_highlight >}}
		- {{< inline_highlight "cs" >}}m{{< /inline_highlight >}} for {{< inline_highlight "cs" >}}decimal{{< /inline_highlight >}}
- when designing APIs, it might be a good idea to do {{< inline_highlight "cs" >}}Int32{{< /inline_highlight >}} instead of {{< inline_highlight "cs" >}}int{{< /inline_highlight >}}, so programmers from other languages now exactly what we mean

##### Nullable types
- {{< inline_highlight "cs" >}}int? x{{< /inline_highlight >}} is a nullable variable -- can contain its value, or {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}
- internally implemented as a {{< inline_highlight "cs" >}}struct Nullable<T>{{< /inline_highlight >}} that has {{< inline_highlight "cs" >}}T Value{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}bool HasValue{{< /inline_highlight >}} members
- {{< inline_highlight "cs" >}}bool?{{< /inline_highlight >}}'s {{< inline_highlight "cs" >}}null{{< /inline_highlight >}} value is "i don't know" so we can use {{< inline_highlight "cs" >}}|{{< /inline_highlight >}} and {{< inline_highlight "cs" >}}&{{< /inline_highlight >}} and get results we expect

#### Reference types
- variable is always passed by **reference** (assigning **creates a new reference to it**)
- the variable data is allocated and stored on managed **heaps**
- can only ever be assigned a reference to the heap
- can be {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}
	- actually, since C# 8.0, we can toggle this behavior and forbid it to contain a {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}
	- only gives warnings, since the compiler can't always determine that it's not from static analysis (although we can specify to treat certain warnings as errors)
- contains:
	- {{< inline_highlight "cs" >}}class{{< /inline_highlight >}}es
	- {{< inline_highlight "cs" >}}interface{{< /inline_highlight >}}s
	- arrays
	- delegates
- takes up more memory, since it has to contain:
	- the reference to the heap, where the value is
	- **heap overhead**
		1. which type it is (reference to an instance of the class {{< inline_highlight "cs" >}}MethodTable{{< /inline_highlight >}})
			- is either \(4/8B\), depending on the architecture
		2. syncblock -- related to threads and locking
			- always \(4B\)
		- padded to nearest \(8B\)

##### Arrays
- each new type inherits {{< inline_highlight "cs" >}}System.Array{{< /inline_highlight >}} and is a new .NET type
- is sort of like generic types -- code is generated for each variant

| Action            | Code                                                |
| ---               | ---                                                 |
| create            | {{< inline_highlight "cs" >}}int[] array = new int[size];{{< /inline_highlight >}}                      |
| create statically | {{< inline_highlight "cs" >}}int[] array = {1, 2, 3};{{< /inline_highlight >}}                          |
| fill with stuff   | {{< inline_highlight "cs" >}}Array.Fill(table, -1, 0, 256);{{< /inline_highlight >}}, requires {{< inline_highlight "cs" >}}System{{< /inline_highlight >}} |
| sort              | {{< inline_highlight "cs" >}}Array.Sort(array);{{< /inline_highlight >}}, highly optimized              |
| length            | {{< inline_highlight "cs" >}}.Length{{< /inline_highlight >}}                                           |

- array of {{< inline_highlight "cs" >}}struct{{< /inline_highlight >}} automatically calls constructors on them so we don't have to
- array of {{< inline_highlight "cs" >}}class{{< /inline_highlight >}} is {{< inline_highlight "cs" >}}null{{< /inline_highlight >}} by default
- **jagged** multidimensional arrays:
	- {{< inline_highlight "cs" >}}int[][] a = new int[2][]{{< /inline_highlight >}}
	- can have different row lengths
	- takes a lot of memory (each row is a pointer) and is not generally nice to it
- **rectangular** multidimensional arrays:
	- single memory object
	- has to have same row lengths
	- nicer to memory
	- {{< inline_highlight "cs" >}}int[,] a = new int[2, 3]{{< /inline_highlight >}}

#### (un)boxing
- crossing the bounday between a reference type and a value type
- {{< inline_highlight "cs" >}}object o = 5;{{< /inline_highlight >}} creates a new object on the heap where the reference points to
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
- defined using the {{< inline_highlight "cs" >}}delegate{{< /inline_highlight >}} keyword

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

- they can also be generic: {{< inline_highlight "cs" >}}delegate bool Condition<T>(T t){{< /inline_highlight >}}

#### Lambda funtions
- functions defined using an expression: {{< inline_highlight "cs" >}}parameters => expression{{< /inline_highlight >}}
- can be converted into a delegate -- {{< inline_highlight "cs" >}}IsEven{{< /inline_highlight >}} above would be {{< inline_highlight "cs" >}}i => i % 2 == 0{{< /inline_highlight >}}

### Structures
- only makes sense when we want the value semantics but more complex behavior
	- {{< inline_highlight "cs" >}}Vector{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}Color{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}Complex{{< /inline_highlight >}} structures, for example
- **no inheritance,** since the variable is always the value -- assigning to variables would be broken (and is one of the main reasons for inheritance), which means:
	- no {{< inline_highlight "cs" >}}abstract{{< /inline_highlight >}}, no {{< inline_highlight "cs" >}}virtual{{< /inline_highlight >}} methods -- all user-defined structures are essentially sealed
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

- careful with putting them in {{< inline_highlight "cs" >}}List<S>{{< /inline_highlight >}} (or some other structure) and making them mutable -- if we attempt to do something like {{< inline_highlight "cs" >}}myList[i].IncreaseByOne(){{< /inline_highlight >}}, it will just modify the returned copy and not do anything
	- this **doesn't happen with arrays**, since they're not using an indexer
	- it's generally a good idea to make structures immutable, because users will use it like this

### Visibility

| Access Modifiers     | Access is...                                            |
| --:                  | ---                                                     |
| {{< inline_highlight "cs" >}}public{{< /inline_highlight >}}             | not restricted.                                         |
| {{< inline_highlight "cs" >}}private{{< /inline_highlight >}}            | limited to the containing type.                         |
| {{< inline_highlight "cs" >}}protected{{< /inline_highlight >}}          | limited to the containing class derived types.          |
| {{< inline_highlight "cs" >}}internal{{< /inline_highlight >}}           | limited to the current assembly.                        |
| {{< inline_highlight "cs" >}}protected internal{{< /inline_highlight >}} | limited to the current assembly OR same/derived types.  |
| {{< inline_highlight "cs" >}}private protected{{< /inline_highlight >}}  | limited to the current assembly AND same/derived types. |

- by default:
	- visibility of classes/interfaces/structs is {{< inline_highlight "cs" >}}internal{{< /inline_highlight >}}
	- visibility in {{< inline_highlight "cs" >}}class{{< /inline_highlight >}}es is {{< inline_highlight "cs" >}}private{{< /inline_highlight >}}
	- visibility in {{< inline_highlight "cs" >}}interface{{< /inline_highlight >}}s is {{< inline_highlight "cs" >}}public{{< /inline_highlight >}}
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

### {{% inline_highlight "cs" %}}readonly{{% /inline_highlight %}}
- used to set fields **not assignable**, except in the **constructor**
- can also be used in autoimplemented properties ({{< inline_highlight "cs" >}}int X { get; } = 5;{{< /inline_highlight >}})

### {{% inline_highlight "cs" %}}=>{{% /inline_highlight %}}
- syntactic sugar for:
	- when a non-{{< inline_highlight "cs" >}}void{{< /inline_highlight >}} method returns something
	- when a void method has only one command

### {{% inline_highlight "cs" %}}??{{% /inline_highlight %}}, {{% inline_highlight "cs" %}}??={{% /inline_highlight %}}, {{% inline_highlight "cs" %}}?.{{% /inline_highlight %}}
- conditional code execution, depending on whether something is {{< inline_highlight "cs" >}}null{{< /inline_highlight >}} or not
- {{< inline_highlight "cs" >}}a ?? b{{< /inline_highlight >}} returns {{< inline_highlight "cs" >}}a{{< /inline_highlight >}}, if it isn't {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}, else {{< inline_highlight "cs" >}}b{{< /inline_highlight >}}
- {{< inline_highlight "cs" >}}x ??= y{{< /inline_highlight >}} will be assigned if {{< inline_highlight "cs" >}}y{{< /inline_highlight >}} isn't {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}
- {{< inline_highlight "cs" >}}x?.m(){{< /inline_highlight >}} will call the method if {{< inline_highlight "cs" >}}x{{< /inline_highlight >}} isn't {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}
- {{< inline_highlight "cs" >}}x?.f{{< /inline_highlight >}} will get the field value, if {{< inline_highlight "cs" >}}x{{< /inline_highlight >}} isn't {{< inline_highlight "cs" >}}null{{< /inline_highlight >}}

#### Arithmetic overflows
```cs
checked {
	// kód
}
```
- is not controlled when functions are called from this block (how could it, when they're probably already translated...)

### References

#### {{% inline_highlight "cs" %}}ref{{% /inline_highlight %}}
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

- calling a method on an object is just a shortcut for doing {{< inline_highlight "cs" >}}Class.function(ref this, <other parameters>){{< /inline_highlight >}}

#### {{% inline_highlight "cs" %}}out{{% /inline_highlight %}}
- an alternative to {{< inline_highlight "cs" >}}ref{{< /inline_highlight >}}
- useful for returning/setting multiple things in a function
- the CIL code is exactly the same, but the compiler checks, whether each {{< inline_highlight "cs" >}}out{{< /inline_highlight >}} parameter has been assigned to (since the caller wouldn't know about the state of the variable)
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

### {{% inline_highlight "cs" %}}var{{% /inline_highlight %}}
- derived at compile time, depending on what is on the right side
- if we can't determine the type, the code won't compile
	- {{< inline_highlight "cs" >}}var x;{{< /inline_highlight >}}
	- {{< inline_highlight "cs" >}}var y = (1, 2, 3);{{< /inline_highlight >}}
	- {{< inline_highlight "cs" >}}var z = null{{< /inline_highlight >}}
- the declaration is a comment -- it's unwise to write {{< inline_highlight "cs" >}}var{{< /inline_highlight >}} everywhere:
	- {{< inline_highlight "cs" >}}var name = GetName();{{< /inline_highlight >}} -- what does it return?
	- {{< inline_highlight "cs" >}}var d = new List<int>();{{< /inline_highlight >}} --  what if I want to change List to a HashSet later (and interface would thus be better to use)?

### Interfaces
- a **contract** -- we can assign any {{< inline_highlight "cs" >}}class{{< /inline_highlight >}} that implements an interface to variables with an interface (when we only require the functionality of the given interface)
	- we can do the same for a {{< inline_highlight "cs" >}}struct{{< /inline_highlight >}}, but it involves boxing

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
	- {{< inline_highlight "cs" >}}OutOfMemoryException{{< /inline_highlight >}} could happen sooner, since we could have a lot of holes in the given heap and the new object wouldn't fit in -- **heap fragmentation**
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
- {{< inline_highlight "cs" >}}GC{{< /inline_highlight >}} class -- for interacting with the GC:
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
	- generally happens for smaller (\(<32\ B\) of machine code) methods that aren't too complicated (no {{< inline_highlight "cs" >}}try/catch{{< /inline_highlight >}}, for example)

#### AOT
- **ahead-of-time** -- before it's needed
- {{< inline_highlight "cs" >}}ngen.exe{{< /inline_highlight >}} -- pre-JITting code
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
	- {{< inline_highlight "cs" >}}sbyte{{< /inline_highlight >}}, {{< inline_highlight "cs" >}}ushort{{< /inline_highlight >}} are not compliant, so making them parameters of a function called from some other DLL might not be the best idea; on the other hand, implementation details are quite fine

#### {{% inline_highlight "cs" %}}typeof(Class){{% /inline_highlight %}}
- return the {{< inline_highlight "cs" >}}Type{{< /inline_highlight >}} instance of the class
- useful when we're comparing types of variables

#### {{% inline_highlight "cs" %}}nameof(x){{% /inline_highlight %}} [[Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/operators/nameof)]
- useful when debugging, when showing exceptions to users...
- better to do than {{< inline_highlight "cs" >}}"x"{{< /inline_highlight >}}, since we can rename using any IDE easily

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
- {{< inline_highlight "cs" >}}using System.Collections.Generic;{{< /inline_highlight >}}

| Action   | Code                                                   |
| ---      | ---                                                    |
| create   | {{< inline_highlight "cs" >}}Dictionary<int, int> d = new Dictionary<int, int>();{{< /inline_highlight >}} |
| contains | {{< inline_highlight "cs" >}}d.ContainsKey(element);{{< /inline_highlight >}}                              |
| add      | {{< inline_highlight "cs" >}}d[index] = element;{{< /inline_highlight >}}                                  |

#### Queues

| Action | Code                                         |
| ---    | ---                                          |
| create | {{< inline_highlight "cs" >}}Queue<string> q = new Queue<string>();{{< /inline_highlight >}}     |
| add    | {{< inline_highlight "cs" >}}q.Enqueue(element);{{< /inline_highlight >}}                        |
| pop    | {{< inline_highlight "cs" >}}q.Dequeue(element);{{< /inline_highlight >}}                        |
| size   | {{< inline_highlight "cs" >}}q.Count;{{< /inline_highlight >}}                                   |
| peek   | {{< inline_highlight "cs" >}}q.Peek();{{< /inline_highlight >}}                                  |

### Acknowledgements
- Adam Dingle, whose [Programming 2 notes](/poznamky/priprava-na-statnice-mff-uk/prog2.pdf) I've shamelessly copied (for certain examples)
