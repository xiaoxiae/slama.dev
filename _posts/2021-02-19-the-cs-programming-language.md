---
title: The C# programming language
category: "notes"
category_icon: /assets/category-icons/mff.webp
excerpt: Lecture notes from The C# programming language lecture (Pavel Ježek, 2020/2021).
---

- .
{:toc}

{% lecture_notes_preface Pavel Ježek | 2020/2021 | MFF %}

Besides this, they have been slightly extended by some C#-specific questions for my [Bachelor's state exam](https://slama.dev/vzdelani/priprava-na-statnice-mff-uk/) that were not covered in the lecture, namely generics and functional elements.

### Strings
- internally an array of chars
- **immutable** (neither length nor contents)
	- concatenation creates new strings
		- {% ihighlight cs %}String.concat(s1, s2, s3, ...);{% endihighlight %} is good for concatenating a lot of them
			- {% ihighlight cs %}s = "a" + "bcd" + "ef";{% endihighlight %} internally uses this method, so it isn't slow
- {% ihighlight cs %}System.String{% endihighlight %} is the same as {% ihighlight cs %}string{% endihighlight %}
	- can't ever be a name of a variable!
	- removes the confusion -- what if someone decides to implement a {% ihighlight cs %}String{% endihighlight %} class
- {% ihighlight cs %}=={% endihighlight %} compares contents, char by char (same as {% ihighlight cs %}.Equals(){% endihighlight %})
	- we can use {% ihighlight cs %}object.ReferenceEquals(o1, o2){% endihighlight %} if we want reference equality

| Action                       | Code                                             |
| ---                          | ---                                              |
| split                        | {% ihighlight cs %}s.Split(char);{% endihighlight %}                                 |
| split on multiple delimiters | {% ihighlight cs %}s.Split(delimiters);{% endihighlight %}, {% ihighlight cs %}delimiters{% endihighlight %} is {% ihighlight cs %}char[]{% endihighlight %} |
| convert to integer           | {% ihighlight cs %}int.Parse(string);{% endihighlight %}, can throw!                 |
| length                       | {% ihighlight cs %}s.Length;{% endihighlight %}                                      |

#### Interning
- hashmap for reusing already created strings
- only for constants, not variables (only exception being {% ihighlight cs %}""{% endihighlight %})!
- we can do this ourselves using {% ihighlight cs %}String.Intern(str);{% endihighlight %} -- if the table contains it, return it; else add it to the table
	- should be limited use: strings can't be removed from the table

#### {% ihighlight cs %}System.Text.StringBuilder{% endihighlight %}
- essentially a **mutable string**
- internally behaves like a dynamic array
	- quick operations like concatenation
- {% ihighlight cs %}.ToString(){% endihighlight %} returns a proper string (since we can't use {% ihighlight cs %}StringBuilder{% endihighlight %} anywhere we want a string)
	- no copying happens -- internally, the new string points to the contents of the {% ihighlight cs %}StringBuilder{% endihighlight %} (so we don't have to copy twice)
	- if we were to modify the string builder again, it gets copied

#### Interpolation
- {% ihighlight cs %}Console.Write("cislo = {0} a {1}", i, j");{% endihighlight %}
	- same as {% ihighlight cs %}Console.Write("cislo = " + i.ToString() + " a " + j.ToString()){% endihighlight %},
	- calls {% ihighlight cs %}String.Format("format string", i, j){% endihighlight %}
		- creates new string

```cs
Console.WriteLine("{0}: Hello, {1}!", s1, s2);

// careful, what if s2 == "{0}"
Console.WriteLine("{0}: Hello, " + s2 + "!", s1, s2);
```

- **interpolated strings** -- {% ihighlight cs %}$"My name is {name} and I'm {age}."{% endihighlight %}
	- is translated into a {% ihighlight cs %}String.Format{% endihighlight %} call (at compile time)... most of the time
	- if assigned to a {% ihighlight cs %}FormattableString{% endihighlight %}, its instance is created instead
		- {% ihighlight cs %}.GetArgument(i){% endihighlight %} returns the i-th argument
		- {% ihighlight cs %}.Format(){% endihighlight %} creates a string
	- the {% ihighlight cs %}{}{% endihighlight %} blocks can be additionaly formatted using {% ihighlight cs %}:<format>{% endihighlight %} and {% ihighlight cs %}, <format>{% endihighlight %}

### Chars
- {% ihighlight cs %}System.Char{% endihighlight %} == {% ihighlight cs %}char{% endihighlight %} (keyword)
- 2-byte UTF-16 character
	- some characters must be at least a string, since some UTF-16 characters can be up to 4 bytes
- {% ihighlight cs %}\xABCD{% endihighlight %} -- unicode code in hex, consumes **one to four hex characters**
- {% ihighlight cs %}\uABCD{% endihighlight %} -- unicode code in hex, consumes **exactly four hex characters**
- {% ihighlight cs %}\UABCDEFGH{% endihighlight %} -- unicode code in hex, consumes **exactly eight hex characters**
	- note that while it does mean a single character, this has to be a string

### File I/O

- if we're dealing with binary I/O, use {% ihighlight cs %}FileStream{% endihighlight %} instead; this is for text

| Action     | Code                                                              |
| ---        | ---                                                               |
| reading    | {% ihighlight cs %}System.IO.StreamReader f = new System.IO.StreamReader(path);{% endihighlight %}    |
| read line  | {% ihighlight cs %}f.ReadLine();{% endihighlight %}                                                   |
| read chars | {% ihighlight cs %}int chars_read = f.Read(buffer, 0, BUFFER_SIZE);{% endihighlight %}                |
| writing    | {% ihighlight cs %}System.IO.StreamWriter f = new System.IO.StreamWriter(path);{% endihighlight %}    |
| write line | {% ihighlight cs %}f.WriteLine(line);{% endihighlight %}                                              |
| close      | {% ihighlight cs %}f.Dispose();{% endihighlight %}                                                    |

### Classes

#### Constructor
- same syntax as C++, but it's a good idea to add a {% ihighlight cs %}public{% endihighlight %} before it
- if none is specified, a default one without parameters is created
	- note that we have to write it explicitly if we want it besides one with parameters!
- translated to a {% ihighlight cs %}.ctor{% endihighlight %} method (see disassembly)
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

- everything in C# inherits {% ihighlight cs %}: object == System.Object{% endihighlight %} (if not inheriting anything)

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
	- {% ihighlight cs %}A(): this(constructor parameters) {}{% endihighlight %}
	- the stuff that would be called before {% ihighlight cs %}A(){% endihighlight %} isn't called (so we don't do it twice)

#### Static/class constructor
- same as a regular constructor but for static variables
- called before the first time an object of the class is instantiated
	- if no object is constructed, it is never called
	- if we do {% ihighlight cs %}Class a;{% endihighlight %}, then it's also not called!
- if none is specified, a default blank one is instantiated
	- this means that it can never have parameters
- internally called {% ihighlight cs %}.cctor{% endihighlight %}

```cs
class A {
	static A() { }
}
```

#### Destructors/finalizers
- same name as the class, but prepended with a tilde ({% ihighlight cs %}~{% endihighlight %})
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
	- if none is specified, {% ihighlight cs %}System.Object == object{% endihighlight %} is used automatically

##### Virtual/abstract/new methods
- it sometimes makes sense to implement a function differently in a child... **member hiding**
	- if we're looking at {% ihighlight cs %}B{% endihighlight %} like it's {% ihighlight cs %}A{% endihighlight %}, the {% ihighlight cs %}A{% endihighlight %} implementation would be called (if it's not virtual)
	- a warning is issued -- did we really want to do this?
		- what if we called the method from some other method in {% ihighlight cs %}A{% endihighlight %}?
		- we can use {% ihighlight cs %}new{% endihighlight %} to let it know that we really wanted to do this

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

- {% ihighlight cs %}new{% endihighlight %} **creates a new record,** {% ihighlight cs %}override{% endihighlight %} **overrides the current one:**
	- it doesn't matter that a method with the same name already existed

|          | {% ihighlight cs %}A{% endihighlight %} | {% ihighlight cs %}M{% endihighlight %} | {% ihighlight cs %}D{% endihighlight %} | {% ihighlight cs %}B{% endihighlight %} |
| ---      | --- | --- | --- | --- |
| {% ihighlight cs %}A.Name{% endihighlight %} | {% ihighlight cs %}A{% endihighlight %} | {% ihighlight cs %}M{% endihighlight %} | {% ihighlight cs %}M{% endihighlight %} | {% ihighlight cs %}M{% endihighlight %} |
| {% ihighlight cs %}D.Name{% endihighlight %} |     |     | {% ihighlight cs %}D{% endihighlight %} | {% ihighlight cs %}B{% endihighlight %} |

- if {% ihighlight cs %}abstract{% endihighlight %} is used, an entry in VTM is created but no implementation is provided
	- the entire class has to be {% ihighlight cs %}abstract{% endihighlight %} so it can't be instantiated, since the method has to be overriden
- virtual methods can be called from the constructor and act correctly, since {% ihighlight cs %}Type{% endihighlight %} (and its VMT) must have been initialized by then
- {% ihighlight cs %}virtual{% endihighlight %} is essentially a promise to the user that it's fine to provide an alternate implementation in the child without breaking the entire class
- {% ihighlight cs %}base{% endihighlight %} can be used to call a method from the parent non-virtually (even if it were)

##### Superclass to subclass conversion
- take {% ihighlight cs %}A{% endihighlight %} and {% ihighlight cs %}B{% endihighlight %} from the code above; {% ihighlight cs %}B b = (B)a;{% endihighlight %} has to be checked at runtime
	- the conversion is explicit, because it's something to think about
- if it's wrong {% ihighlight cs %}InvalidCastException{% endihighlight %} is thrown, so test the code!

###### {% ihighlight cs %}is{% endihighlight %}
- checks, whether {% ihighlight cs %}object{% endihighlight %} is of the given {% ihighlight cs %}Type{% endihighlight %} (or type of any of its children)
- runtime calls a method, not too quick of an operation -- has to go through the class tree!
- if {% ihighlight cs %}object{% endihighlight %} is {% ihighlight cs %}null{% endihighlight %}, {% ihighlight cs %}false{% endihighlight %} is always returned, though it seems that {% ihighlight cs %}null{% endihighlight %} can be anything

###### {% ihighlight cs %}as{% endihighlight %}
- returns the {% ihighlight cs %}object{% endihighlight %} if it is of the given {% ihighlight cs %}Type{% endihighlight %} (or type of any of its children), else {% ihighlight cs %}null{% endihighlight %}

```cs
B b = a as B;  // assigns {% ihighlight cs %}a{% endihighlight %} to {% ihighlight cs %}b{% endihighlight %} if it's of the valid type
               // this is the reason why {% ihighlight cs %}null is A{% endihighlight %} returns false

if (b != null) {
	// do stuff with {% ihighlight cs %}B b{% endihighlight %}
}

// is almost equivalent to (since C# 7.0)
// only difference is that {% ihighlight cs %}b{% endihighlight %} is not initialized after

if (a is B b) {
	// do stuff with {% ihighlight cs %}B b{% endihighlight %}
}
```

##### {% ihighlight cs %}System.Object{% endihighlight %}
- inherited by all classes
- has the following members:
	- {% ihighlight cs %}protected object MemberwiseClone();{% endihighlight %}
		- creates a shallow copy of the object (byte by byte)
		- doesn't make much sense for reference types
		- note that it is protected!
			- implement {% ihighlight cs %}public A Clone() {...}{% endihighlight %} to make it public
			- there is an {% ihighlight cs %}IClonable{% endihighlight %} interface, but it was before {% ihighlight cs %}<T>{% endihighlight %}...
	- {% ihighlight cs %}public Type GetType();{% endihighlight %}
		- done for all types ({% ihighlight cs %}new Type("A"){% endihighlight %},...)
		- contains {% ihighlight cs %}.Name{% endihighlight %} and other stuff for reflection
		- also contains a **virtual method table** (VMT)
	- {% ihighlight cs %}public virtual bool Equals(object o);{% endihighlight %}
		- for checking, whether two objects are equal
	- {% ihighlight cs %}public virtual string ToString();{% endihighlight %}
		- the string representation of the object
		- shouldn't be something too complicated (like a giant recursive function)
	- {% ihighlight cs %}public virtual int GetHashCode();{% endihighlight %}
		- hash code of the object; for hashmap-like data structures
	- {% ihighlight cs %}public static bool ReferenceEquals(object objA, object objB);{% endihighlight %}
		- whether the two objects are equal by reference

##### {% ihighlight cs %}System.ValueType{% endihighlight %}
- is inherited by all types ({% ihighlight cs %}int{% endihighlight %}, {% ihighlight cs %}Nullable{% endihighlight %}, {% ihighlight cs %}bool{% endihighlight %}, user-defined structures...)
- overrides {% ihighlight cs %}Equals{% endihighlight %} to be byte-equal (since it is a value type)
	- if it has reference members, **uses reflection to check their values too** -- string, for example
		- better to implement it ourselves in this case

##### {% ihighlight cs %}sealed{% endihighlight %}
- prevents inheritance and allows for some code optimizations
	- no virtual function calls
- {% ihighlight cs %}sealed class A {}{% endihighlight %} -- is not inheritable
- {% ihighlight cs %}sealed override void m(){% endihighlight %} -- is not overridable

#### Generic classes
- useful when we have a lot of similar classes that differ by types
- can be used for {% ihighlight cs %}struct{% endihighlight %}s and {% ihighlight cs %}interface{% endihighlight %}s too

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
- all exceptions must inherit the {% ihighlight cs %}System.Exception{% endihighlight %} class
	- even the ones from other languages are wrapped in a {% ihighlight cs %}SEHException{% endihighlight %}
- takes a _long_ time (a lot of things have to be collected), though a {% ihighlight cs %}try{% endihighlight %} block is basically free
- watch out for exceptions that
	1. can't be caught (like {% ihighlight cs %}StackOverflowException{% endihighlight %})
	2. probably shouldn't be caught (like {% ihighlight cs %}OutOfMemoryException{% endihighlight %})

#### {% ihighlight cs %}System.Exception{% endihighlight %}

| Property/Function | Meaning                             |
| ---               | ---                                 |
| {% ihighlight cs %}e.Message{% endihighlight %}       | {% ihighlight cs %}string{% endihighlight %} error message              |
| {% ihighlight cs %}e.StackTrace{% endihighlight %}    | {% ihighlight cs %}string{% endihighlight %} trace of method call stack |
| {% ihighlight cs %}e.Source{% endihighlight %}        | {% ihighlight cs %}string{% endihighlight %} app/object that threw it   |
| {% ihighlight cs %}e.ToString(){% endihighlight %}    | {% ihighlight cs %}string{% endihighlight %} the formatted exception    |

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
- it's important to distinguish exceptions due to bugs ({% ihighlight cs %}NullReferenceException{% endihighlight %}, {% ihighlight cs %}IndexOutOfRangeException{% endihighlight %}) and due to incorrect program usage (possibly {% ihighlight cs %}FileNotFoundException{% endihighlight %} and many others)

---

- {% ihighlight cs %}Exception{% endihighlight %}
	- {% ihighlight cs %}SystemException{% endihighlight %}
		- {% ihighlight cs %}ArithmeticException{% endihighlight %}
			- {% ihighlight cs %}DivideByZeroException{% endihighlight %}
			- {% ihighlight cs %}OverflowException{% endihighlight %}
			- ....
		- {% ihighlight cs %}NullReferenceException{% endihighlight %}
		- {% ihighlight cs %}IndexOutOfRangeException{% endihighlight %}
		- {% ihighlight cs %}InvalidCastException{% endihighlight %}
		- ...
	- {% ihighlight cs %}ApplicationException{% endihighlight %}
		- user-defined exceptions
		- ...
	- {% ihighlight cs %}IOException{% endihighlight %}
		- {% ihighlight cs %}FileNotFoundException{% endihighlight %}
		- {% ihighlight cs %}DirectoryNotFoundException{% endihighlight %}
		- ...
	- {% ihighlight cs %}WebException{% endihighlight %}
	- ...


### {% ihighlight cs %}using{% endihighlight %}
```cs
Type x;
try {
	x = new Type();  // could raise an exception!

	// some code
} finally {
	if (x != null) x.Dispose();
}
```
- is (sort of, because {% ihighlight cs %}x{% endihighlight %} has a slightly different scope) equivalent to

```cs
using (type x = new Type()) {
	// some code
}
```

- is also equivalent to (since C# 8.0, with {% ihighlight cs %}Dispose{% endihighlight %} being called when {% ihighlight cs %}x{% endihighlight %} goes out of scope)

```cs
using type x = new Type();
```

- only works with objects that inherit {% ihighlight cs %}IDisposable{% endihighlight %} \(\implies\) have a {% ihighlight cs %}Dispose{% endihighlight %} method

### Properties

```cs
T Property {
	get { /* stuff to do */ }
	set { /* stuff to do (with a variable {% ihighlight cs %}value{% endihighlight %}) */ }
}
```

- syntactic sugar for defining a {% ihighlight cs %}T get(){% endihighlight %} and {% ihighlight cs %}void set(T value){% endihighlight %} methods
	- must be used with {% ihighlight cs %}={% endihighlight %}, although it does generate methods {% ihighlight cs %}get_*{% endihighlight %} and {% ihighlight cs %}set_*{% endihighlight %} (so don't name other methods like that)
- is nice when we want to let the programmer know that we're just setting/getting something (although it may do something more complex)
	- it's generally a good idea to not make it too slow, since the syntax looks instant
-  when doing assemblies, properties make it so we don't need to rebuild code that uses it, since the API stays the same (which can be desirable)
- interfaces can also contain them (not the implementation, just that it has to have one)

#### Auto-implemented
- if we're just doing {% ihighlight cs %}get => value{% endihighlight %} and {% ihighlight cs %}set = value{% endihighlight %}, we can just do {% ihighlight cs %}get;{% endihighlight %} and {% ihighlight cs %}set;{% endihighlight %} and the code will get automatically generated
	- what if we want to make an interface out of it in the future?
	- what if we want to add constraints to the values in the future?
- we can also set default values: {% ihighlight cs %}int X { get; set; } = 12;{% endihighlight %}
- we can also explicitly set the accessibility of the functions: {% ihighlight cs %}public int Length { get; private set; }{% endihighlight %}
	- {% ihighlight cs %}public{% endihighlight %} affects {% ihighlight cs %}get{% endihighlight %}, since it doesn't have an explicit modifier, but not {% ihighlight cs %}set{% endihighlight %}, because it has one

#### Read-only
- {% ihighlight cs %}set{% endihighlight %} can be omitted, which makes the property read-only
- this means it can only be changed in the constructor and nowhere else

#### Instantiating objects with properties
```cs
A a = new A { x = 3; y = 6 };

// is literally the same as

A a = new A();
a.x = 3;
a.y = 6;
```

- this implies that the setter can't be {% ihighlight cs %}private{% endihighlight %}, since it's just syntactic sugar!

#### Parametric properties (indexers)
- for defining indexing on an object of the given class
- can be overloaded, since it's just a method (but might not be the smartest thing to do)
- are compiled into {% ihighlight cs %}get_Item{% endihighlight %} and {% ihighlight cs %}set_Item{% endihighlight %}

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
	- {% ihighlight cs %}struct{% endihighlight %}ures
	- simple types ({% ihighlight cs %}int{% endihighlight %}, {% ihighlight cs %}char{% endihighlight %})
	- {% ihighlight cs %}Nullable{% endihighlight %}s (it's just a struct)
	- enumerations
	- is weird, since it's completely different to references that are allocated
- **can implement interfaces**, but boxing happens when we assign to {% ihighlight cs %}I var{% endihighlight %}
	- watch out for passing stuctures to function and doing something to them, since they will be boxed and nothing will change...

##### Simple types
- things like {% ihighlight cs %}byte{% endihighlight %}, {% ihighlight cs %}short{% endihighlight %}, {% ihighlight cs %}int{% endihighlight %}, {% ihighlight cs %}char{% endihighlight %}, {% ihighlight cs %}bool{% endihighlight %}...
- CLR and JIT knows about it, so operators (think {% ihighlight cs %}+{% endihighlight %}) is not a function call
- sizes are (almost) always defined (not like C++), except:
	- {% ihighlight cs %}nint{% endihighlight %} and {% ihighlight cs %}nuint{% endihighlight %} -- native, platform-dependent {% ihighlight cs %}(u)int{% endihighlight %} (since C# 9.0)
	- {% ihighlight cs %}bool{% endihighlight %} is only {% ihighlight cs %}true/false{% endihighlight %}, so it isn't defined too (implementation detail)
- {% ihighlight cs %}decimal{% endihighlight %} -- exponent is decimal, so numbers like {% ihighlight cs %}0.1{% endihighlight %} are precies
	- the downside is that it is much slower
- all of them are perpendicular to one another in the type hierarchy, but there **are conversions**
	- it is an actual conversion, not like for reference types (just checks in that case)
	- **implicit** conversions happen automatically, while **explicit** are manual
		- although a conversion is implicit, it can have data loss ({% ihighlight cs %}long{% endihighlight %} \(\rightarrow\) {% ihighlight cs %}float{% endihighlight %})
	- they are **not free,** it can sometimes take quite a while ({% ihighlight cs %}int{% endihighlight %} \(\rightarrow\) {% ihighlight cs %}float{% endihighlight %})
	- no conversions from/to {% ihighlight cs %}bool{% endihighlight %}

![Implicit Conversions.](/assets/the-cs-programming-language/implicit-conversions.svg)

- by default, all numeric constants (without a period) are {% ihighlight cs %}int{% endihighlight %}
	- however, we can do {% ihighlight cs %}long a = 10;{% endihighlight %}, it's optimized to not do a conversion
	- when a specific constant type is desired, we can use the following suffixes:
		- unsigned int/long: {% ihighlight cs %}u{% endihighlight %}
		- long, unsigned long: {% ihighlight cs %}l{% endihighlight %}
		- unsigned long: {% ihighlight cs %}ul{% endihighlight %}
- by default, all decimal number constants are {% ihighlight cs %}double{% endihighlight %}
	- we **can't do** {% ihighlight cs %}float f = 2.5;{% endihighlight %} (but must do {% ihighlight cs %}2.5f{% endihighlight %})
	- other suffixes include
		- {% ihighlight cs %}d{% endihighlight %} for {% ihighlight cs %}double{% endihighlight %}
		- {% ihighlight cs %}m{% endihighlight %} for {% ihighlight cs %}decimal{% endihighlight %}
- when designing APIs, it might be a good idea to do {% ihighlight cs %}Int32{% endihighlight %} instead of {% ihighlight cs %}int{% endihighlight %}, so programmers from other languages now exactly what we mean

##### Nullable types
- {% ihighlight cs %}int? x{% endihighlight %} is a nullable variable -- can contain its value, or {% ihighlight cs %}null{% endihighlight %}
- internally imlemented as a {% ihighlight cs %}struct Nullable<T>{% endihighlight %} that has {% ihighlight cs %}T Value{% endihighlight %} and {% ihighlight cs %}bool HasValue{% endihighlight %} memobers
- {% ihighlight cs %}bool?{% endihighlight %}'s {% ihighlight cs %}null{% endihighlight %} value is "i don't know" so we can use {% ihighlight cs %}|{% endihighlight %} and {% ihighlight cs %}&{% endihighlight %} and get results we expect

#### Reference types
- variable is always passed by **reference** (assigning **creates a new reference to it**)
- the variable data is allocated and stored on managed **heaps**
- can only ever be assigned a reference to the heap
- can be {% ihighlight cs %}null{% endihighlight %}
	- actually, since C# 8.0, we can toggle this behavior and forbid it to contain a {% ihighlight cs %}null{% endihighlight %}
	- only gives warnings, since the compiler can't always determine that it's not from static analysis (although we can specify to treat certain warnings as errors)
- contains:
	- {% ihighlight cs %}class{% endihighlight %}es
	- {% ihighlight cs %}interface{% endihighlight %}s
	- arrays
	- delegates
- takes up more memory, since it has to contain:
	- the reference to the heap, where the value is
	- **heap overhead**
		1. which type it is (reference to an instance of the class {% ihighlight cs %}MethodTable{% endihighlight %})
			- is either \(4/8B\), depending on the architecture
		2. syncblock -- related to threads and locking
			- always \(4B\)
		- padded to nearest \(8B\)

##### Arrays
- each new type inherits {% ihighlight cs %}System.Array{% endihighlight %} and is a new .NET type
- is sort of like generic types -- code is generated for each variant

| Action            | Code                                                |
| ---               | ---                                                 |
| create            | {% ihighlight cs %}int[] array = new int[size];{% endihighlight %}                      |
| create statically | {% ihighlight cs %}int[] array = {1, 2, 3};{% endihighlight %}                          |
| fill with stuff   | {% ihighlight cs %}Array.Fill(table, -1, 0, 256);{% endihighlight %}, requires {% ihighlight cs %}System{% endihighlight %} |
| sort              | {% ihighlight cs %}Array.Sort(array);{% endihighlight %}, highly optimized              |
| length            | {% ihighlight cs %}.Length{% endihighlight %}                                           |

- array of {% ihighlight cs %}struct{% endihighlight %} automatically calls constructors on them so we don't have to
- array of {% ihighlight cs %}class{% endihighlight %} is {% ihighlight cs %}null{% endihighlight %} by default
- **jagged** multidimensional arrays:
	- {% ihighlight cs %}int[][] a = new int[2][]{% endihighlight %}
	- can have different row lengths
	- takes a lot of memory (each row is a pointer) and is not generally nice to it
- **rectangular** multidimensional arrays:
	- single memory object
	- has to have same row lengths
	- nicer to memory
	- {% ihighlight cs %}int[,] a = new int[2, 3]{% endihighlight %}

#### (un)boxing
- crossing the bounday between a reference type and a value type
- {% ihighlight cs %}object o = 5;{% endihighlight %} creates a new object on the heap where the reference points to
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
- defined using the {% ihighlight cs %}delegate{% endihighlight %} keyword

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

- they can also be generic: {% ihighlight cs %}delegate bool Condition<T>(T t){% endihighlight %}

#### Lambda funtions
- functions defined using an expression: {% ihighlight cs %}parameters => expression{% endihighlight %}
- can be converted into a delegate -- {% ihighlight cs %}IsEven{% endihighlight %} above would be {% ihighlight cs %}i => i % 2 == 0{% endihighlight %}

### Structures
- only makes sense when we want the value semantics but more complex behavior
	- {% ihighlight cs %}Vector{% endihighlight %}, {% ihighlight cs %}Color{% endihighlight %}, {% ihighlight cs %}Complex{% endihighlight %} structures, for example
- **no inheritance,** since the variable is always the value -- assigning to variables would be broken (and is one of the main reasons for inheritance), which means:
	- no {% ihighlight cs %}abstract{% endihighlight %}, no {% ihighlight cs %}virtual{% endihighlight %} methods -- all user-defined structures are essentially sealed
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

- careful with putting them in {% ihighlight cs %}List<S>{% endihighlight %} (or some other structure) and making them mutable -- if we attempt to do something like {% ihighlight cs %}myList[i].IncreaseByOne(){% endihighlight %}, it will just modify the returned copy and not do anything
	- this **doesn't happen with arrays**, since they're not using an indexer
	- it's generally a good idea to make structures immutable, because users will use it like this

### Visibility

| Access Modifiers     | Access is...                                            |
| --:                  | ---                                                     |
| {% ihighlight cs %}public{% endihighlight %}             | not restricted.                                         |
| {% ihighlight cs %}private{% endihighlight %}            | limited to the containing type.                         |
| {% ihighlight cs %}protected{% endihighlight %}          | limited to the containing class derived types.          |
| {% ihighlight cs %}internal{% endihighlight %}           | limited to the current assembly.                        |
| {% ihighlight cs %}protected internal{% endihighlight %} | limited to the current assembly OR same/derived types.  |
| {% ihighlight cs %}private protected{% endihighlight %}  | limited to the current assembly AND same/derived types. |

- by default:
	- visibility of classes/interfaces/structs is {% ihighlight cs %}internal{% endihighlight %}
	- visibility in {% ihighlight cs %}class{% endihighlight %}es is {% ihighlight cs %}private{% endihighlight %}
	- visibility in {% ihighlight cs %}interface{% endihighlight %}s is {% ihighlight cs %}public{% endihighlight %}
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

### {% ihighlight cs %}readonly{% endihighlight %}
- used to set fields **not assignable**, except in the **constructor**
- can also be used in autoimplemented properties ({% ihighlight cs %}int X { get; } = 5;{% endihighlight %})

### {% ihighlight cs %}=>{% endihighlight %}
- syntactic sugar for:
	- when a non-{% ihighlight cs %}void{% endihighlight %} method returns something
	- when a void method has only one command

### {% ihighlight cs %}??{% endihighlight %}, {% ihighlight cs %}??={% endihighlight %}, {% ihighlight cs %}?.{% endihighlight %}
- conditional code execution, depending on whether something is {% ihighlight cs %}null{% endihighlight %} or not
- {% ihighlight cs %}a ?? b{% endihighlight %} returns {% ihighlight cs %}a{% endihighlight %}, if it isn't {% ihighlight cs %}null{% endihighlight %}, else {% ihighlight cs %}b{% endihighlight %}
- {% ihighlight cs %}x ??= y{% endihighlight %} will be assigned if {% ihighlight cs %}y{% endihighlight %} isn't {% ihighlight cs %}null{% endihighlight %}
- {% ihighlight cs %}x?.m(){% endihighlight %} will call the method if {% ihighlight cs %}x{% endihighlight %} isn't {% ihighlight cs %}null{% endihighlight %}
- {% ihighlight cs %}x?.f{% endihighlight %} will get the field value, if {% ihighlight cs %}x{% endihighlight %} isn't {% ihighlight cs %}null{% endihighlight %}

#### Arithmetic overflows
```cs
checked {
	// kód
}
```
- is not controlled when functions are called from this block (how could it, when they're probably already translated...)

### References

#### {% ihighlight cs %}ref{% endihighlight %}
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

- calling a method on an object is just a shortcut for doing {% ihighlight cs %}Class.function(ref this, <other parameters>){% endihighlight %}

#### {% ihighlight cs %}out{% endihighlight %}
- an alternative to {% ihighlight cs %}ref{% endihighlight %}
- useful for returning/setting multiple things in a function
- the CIL code is exactly the same, but the compiler checks, whether each {% ihighlight cs %}out{% endihighlight %} parameter has been assigned to (since the caller wouldn't know about the state of the variable)
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

### {% ihighlight cs %}var{% endihighlight %}
- derived at compile time, depending on what is on the right side
- if we can't determine the type, the code won't compile
	- {% ihighlight cs %}var x;{% endihighlight %}
	- {% ihighlight cs %}var y = (1, 2, 3);{% endihighlight %}
	- {% ihighlight cs %}var z = null{% endihighlight %}
- the declaration is a comment -- it's unwise to write {% ihighlight cs %}var{% endihighlight %} everywhere:
	- {% ihighlight cs %}var name = GetName();{% endihighlight %} -- what does it return?
	- {% ihighlight cs %}var d = new List<int>();{% endihighlight %} --  what if I want to change List to a HashSet later (and interface would thus be better to use)?

### Interfaces
- a **contract** -- we can assign any {% ihighlight cs %}class{% endihighlight %} that implements an interface to variables with an interface (when we only require the functionality of the given interface)
	- we can do the same for a {% ihighlight cs %}struct{% endihighlight %}, but it involves boxing

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
	- {% ihighlight cs %}OutOfMemoryException{% endihighlight %} could happen sooner, since we could have a lot of holes in the given heap and the new object wouldn't fit in -- **heap fragmentation**
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
- {% ihighlight cs %}GC{% endihighlight %} class -- for interacting with the GC:
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
	- generally happens for smaller (\(<32\ B\) of machine code) methods that aren't too complicated (no {% ihighlight cs %}try/catch{% endihighlight %}, for example)

#### AOT
- **ahead-of-time** -- before it's needed
- {% ihighlight cs %}ngen.exe{% endihighlight %} -- pre-JITting code
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
	- {% ihighlight cs %}sbyte{% endihighlight %}, {% ihighlight cs %}ushort{% endihighlight %} are not compliant, so making them parameters of a function called from some other DLL might not be the best idea; on the other hand, implementation details are quite fine

#### {% ihighlight cs %}typeof(Class){% endihighlight %}
- return the {% ihighlight cs %}Type{% endihighlight %} instance of the class
- useful when we're comparing types of variables

#### {% ihighlight cs %}nameof(x){% endihighlight %} [[Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/operators/nameof)]
- useful when debugging, when showing exceptions to users...
- better to do than {% ihighlight cs %}"x"{% endihighlight %}, since we can rename using any IDE easily

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
- {% ihighlight cs %}using System.Collections.Generic;{% endihighlight %}

| Action   | Code                                                   |
| ---      | ---                                                    |
| create   | {% ihighlight cs %}Dictionary<int, int> d = new Dictionary<int, int>();{% endihighlight %} |
| contains | {% ihighlight cs %}d.ContainsKey(element);{% endihighlight %}                              |
| add      | {% ihighlight cs %}d[index] = element;{% endihighlight %}                                  |

#### Queues

| Action | Code                                         |
| ---    | ---                                          |
| create | {% ihighlight cs %}Queue<string> q = new Queue<string>();{% endihighlight %}     |
| add    | {% ihighlight cs %}q.Enqueue(element);{% endihighlight %}                        |
| pop    | {% ihighlight cs %}q.Dequeue(element);{% endihighlight %}                        |
| size   | {% ihighlight cs %}q.Count;{% endihighlight %}                                   |
| peek   | {% ihighlight cs %}q.Peek();{% endihighlight %}                                  |

### Acknowledgements
- Adam Dingle, whose [Programming 2 notes](/assets/priprava-na-statnice-mff-uk/prog2.pdf) I've shamelessly copied (for certain examples)
