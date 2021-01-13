---
title: C++
---

{% match ### Data structures %}

{% match #### Arrays %}

| Action            | Code                                                    |
| ---               | ---                                                     |
| create (dynamic)  | `int *array = new int[size];`, requires `<new>`         |
| create (constant) | `int array[constant size];`                             |
| fill with stuff   | `fill_n(array, size, element);`, requires `<algorithm>` |


{% match #### Dictionaries %}

- `#include <map>`           -- hashing, constant access
- `#include <unordered_map>` -- R&B trees, {% latex %}\log(n){% endlatex %} access

{% match #### Sets %}

- `#include <set>`      -- usually a binary tree, {% latex %}\log(n){% endlatex %} access
- `#include <hash_set>` -- hashing, constant access


{% match ### Strings %}

| Action                             | Code                           |
| ---                                | ---                            |
| convert to integer                 | `std::stoi(value, &position)` |
| length of string; constant         | `str.length()`                 |
| end is optional                    | `str.substring(start, end)`    |
| look for something, from the left  | `str.find(something)`          |
| look for something, from the right | `str.rfind(something)`         |

#### [`istringstream`](https://www.cplusplus.com/reference/sstream/istringstream/) / [`ostringstream`](https://www.cplusplus.com/reference/sstream/ostringstream/)
- a stream classes on strings
- has all the goodies that a stream class has

| Action              | Code                                                    |
| ---                 | ---                                                     |
| create              | `std::istringstream iss(string);`                       |
| read from/write to  | `iss >> variable`, `oss << variable`                  |
| read till delimiter | `getline(is, line)`, where `line` is a string variable |

{% match ### Chars %}

| Action  | Code                    |
| ---     | ---                     |
| digits  | `std::isdigit(string);` |
| letters | `std::isalpha(string);` |

{% match ### Printing %}
- requires `<iostream>`
- uses the `<<` operator
	- is overloaded for various types (`endl` is a function!)
- `std::cout << "Hello, world!" << std:endl;`

{% match ### File I/O %}

| Action            | Code                                  |
| ---               | ---                                   |
| reading from file | `std::ifstream fin("path/to/file");`  |
| writing to file   | `std::ofstream fout("path/to/file");` |

{% match ### Sorting %}
- `#include <algorithm>`
- `std::sort(RandomAccessIterator first, RandomAccessIterator last, Compare comp)`
	- `comp` not required, default used
	- usually `collection.begin()` and `collection.end()`

{% match ### For each %}
- from C++ 11
```
for (auto && x : p) {
	std::cout << ","
}
```
- `x` is one of the objects from `p` in each iteraton loop
	- without `&&` (magic for now, will be explained later), it would be a copy
	- the actual objects, not references
	- adding +1 to each `x` would work (depends on whether `p` is const)
- `auto` is just a compiler tying -- is replaced by the compiler

### Modules

#### The new way
- `export`, `module`, `import`
- `.ixx` soubory
- import/export jsou chytřejší
- umějí toho více, jako např. definovat implementace
- ještě není úplně jisté, jak se bude importovat standardní knihovna
- norma ještě není úplně pevná, ještě chvilku to potrvá

#### The old (current) way
- use `.hpp` (header) files
- exposes interface of a given cpp file to another one
	- both have to include it for this to do so

```cpp
// world.hpp
// prevent including the same header file twice:
#idndef WORLD_HPP_
#define WORLD_HPP_

#include <vector>
#include <string>

// type definition (like typedef in C):
using t_arg = str::vector<std::string>;

// function declaration
void function();

#endif
```

#### Includes
- pastes the included file to the given file
- careful: `#include "stuff"` and `#include <stuff>` is different
	- implementation detauls -- `""` has a broader scope, `<>` is for std libraries

### Storage and containers
- containers **hold the objects**, not their references
	- not like Python, where appending an object simply puts a reference to it
	- `new` should not be used
		- hide allocation in constructors and methods of the given storage object
		- make it a local variable
- arrays can be dangerous -- reaching outside and even changing the contents will likely not result in an error, since it's a valid memory position where something else is stored...
	- just use `vector` or some other, safer container

### `&`, `const`
- `&` in function argument means that it is passed as a reference
	- makes the code much faster -- we don't have to copy the entire thing (entire `vector` of `string`s, for example)!
	- confusing, since `&` in other context creates pointers
- `const` prevents modification of the argument by the compiler
- [this is a great read](http://duramecho.com/ComputerInformation/WhyHowCppConst.html) to understand what `const` does in various contexts

```cpp
// world.hpp
...
void world(const t_arg & p);
...
```

### References/pointers/links to stuff

#### References
- built-in to C++
- pointing at an object when initialized, **can't be redirected**
- identical (in use) with values (`r.a`)
- can be one of three types:
	- **(modifiable) L-value reference** (`T &`) -- the value must be an **L-value**
	- **constant reference** (`const T &`) -- any object of type `T`
	- **R-value reference** (`T &&`) -- the value must be **R-value**

#### Pointers

##### Raw (`*`)
- built-in to C/C++
- pointer arithmetics to access additional values in an array
- special operators to access the value -- either `*p` or `p->a`
- **manual deallocation** -- not great to use for ownership

##### Smart (`std::shared_ptr<T>, std::unique_ptr<T>`)
- template classes in the standard C++ library
- introduced because pointers in C were the main root of most of problems regarding security, memory,...
- (mostly the) same arithmetics as with `*`, but not really needed (see iterators)
- **automatic ownership** -- meant to be used for ownership
	- implemented using **reference counting**
		- different than garbage collecting -- the objects are recycled immediately

##### Iterators (`K::iterator, K::const_iterator`)
- connected to the given container
- the arithmetics don't just access the adjacent element, but can have a more complex behavior (go to next element in the tree)

#### Passing to functions (TODO: more on this later)
- if we want to modify the argument -- pass by **L-value reference** (`T &`)
- else if copying is cheap (int, pointer, small struct) -- pass by **value** (`T`)
- else if the type doesn't support modifying -- pass by **R-value reference** (`T &&`)
- else if we want to store a copy of the parameter:
	- if we care about speed, implement both `const T &` and `T &&`
	- simplified: pass by value (`T`) and use `std::move()` when saving
- else pass by **constant reference**

#### Returning from functions
- if a function makes an object accessible (`arr[]`)
	- if we want to allow modifying the object, return by **L-value reference** (`T &`)
	- else use **constant reference** (`const T &`)
	- _the object must survive at least for a bit when returning from the function_
		- if we're returning by reference and creating new data, this will never work
- else return **value** (`T`)
	- is (at least recently) quite fast -- **copy/move-elision**
		- without it, the function would be rewritten with a new pointer parameter where to return the value from the function; 

{% match ### Classes %}

#### Uninstantiated

```cpp
class X{
public:
	class N { /*...*/ };
	
	typedef unsigned long t;
	using t2 = int;
	
	static constexpr t c = 1;  // must be static
	                           // since C++ 11 -- const is a runtime guard against modification
	static int f(int p) { return p + 1; }
```

- can't be instantiated (no object creation)
- basically a box for data
- can be accessed using `X::`
- similar to `namespace`, but with a few differences:
	- can be `public/protected/private`
	- can be split into multiple header files
	- can be made directly visible (`using namespace`)
		- better to do `using namespace::identifier`
		- **argument-dependent lookup** -- functions from a namespace may be visible even without `using`
		- `using` on functiosn does not hide previously visible versions
		- necessary, because of operators... (if we want to connect strings with `std::+`)
- prevents collisions for other identifiers
- can be as a parameter for a template

#### Value types

```cpp
public:
	Y() : m_(0) {}
	int get_m() const {return m_;}
	void set_m(int m) {m_ = m;}
private:
	int m_;
```

- `Y v1;` is **not a reference**, it's the actual object
	- an array of those holds the actual data of the class, not pointers
	- use `std::unique_ptr<Y> p;` or `new` for pointers
	- access via `.` or `->`, depending on pointer or not
- when an object is given another object of its type as a parameter, it can **access its private members**
	- important -- copy-constructor couldn't be able to touch the data it needs
- [`protected`](https://docs.microsoft.com/en-us/cpp/cpp/protected-cpp?view=msvc-160) -- a successor can touch data of a predecessor, but they are not visible outside
	- not too frequently used
- if an object is `const`, only `const` methods can be invoked (and `const` members can be accessed)
	- if a member is `mutable`, it can be modified (how many references point to an object?)

#### Inheritance + virtual functions

```cpp
class Base { /*...*/ };
class Derived : public Base { /*...*/ };
```

- `Derived` obsahuje všechny datové položky i metody třídy `Base`
	- je možné doplnit další, není vhodné překrývat staré
	- je možné měnit chování metod, které jsou deklarovány `virtual` (překladač to musí vědět)

```cpp
class Base {
	virtual ~Base() noexcept {}
	virtual void f () { /*...*/ }
};

class Derived final : public Base {
	virtual void f() override { /*...*/ }
}
```

- `final` -- no more inheritance from this class
	- can be also used in a function to forbid redefining it in successors
- `override` -- makes compiler check that this virtual method exists in some predecessor
- if we actually want to make inheritance work, we need **pointers, not objects**
	- a vector of `Base` doesn't make sense
	- calling a function on a pointer of type predecessor but whose value is the successor will invoke the successor implementation

```cpp
Derived d;
d.f();      // calls Derived::f, even if it wasn't virtual

Base b = d;
d.f();      // calls Base:f, even if it was virtual
            // Base should usually be abstract so this doesn't compile
```

#### Abstract (vs. concrete)
- contains at least one purely virtual function
- can't be instantiated

```cpp
class Base {
	// ...
	virtual void f() = 0;
}
```

- useful to contain a virtual destructor, so successors have to implement it
- `noexcept` will guarantee that this operation won't cause exceptions
