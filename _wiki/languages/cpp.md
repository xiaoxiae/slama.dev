---
title: C++
---

{% match ### Data structures %}

{% match #### Arrays %}

| Action          | Code                                                   |
| ---             | ---                                                    |
| create          | `int *array = new int[size];`, requires `<new>`        |
| fill with stuff | `fill_n(array, size, element)`, requires `<algorithm>` |


{% match #### Dictionaries %}

| Class                      | Behavior                 |
| ---                        | ---                      |
| `#include <map>`           | hashing, constant access |
| `#include <unordered_map>` | R&B trees, log(n) access |

| Action   | Code                  |
| ---      | ---                   |
| create   | `map<int, int> m;`    |
| contains | `m.count(element);`   |
| add      | `m[index] = element;` |


{% match ### Strings %}

| Action | Code          |
| ---    | ---           |
| length | `s.length();` |

{% match ### Printing %}
- requires `<iostream>`
- uses the `<<` operator
	- is overloaded for various types (`endl` is a function!)
- `std::cout << "Hello, world!" << std:endl;`

{% match ### Sorting %}
- `#include <algorithm>`
- `std::sort(RandomAccessIterator first, RandomAccessIterator last, Compare comp)`
	- `comp` not required, default used
	- usually `vector.begin()` and `vector.end()`

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

---

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

```hpp
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

```hpp
// world.hpp
...
void world(const t_arg & p);
...
```

### Values/pointers/references
- classes/struct are created/copied by value

#### Values
- `Beast x` _is_ a value
- assignments are by value

#### Pointers
- C-style `*` or C++-style `std::shared_ptr`
	- if we don't care about the lifetime of an object, use `*`
	- if we do, use `std::stared_ptr` (since if no smart pointers are pointing to an objec, it gets taken care of)

#### References
- when we want to hold and modify some object, but not care about its lifetime
- `Beast & x = some_beast(100);`
- act as the objects (`x.health -= 50`)
- assignment acts as value
- is deleted by someone else who owns them
- not like in Java -- we can iterate over a container and change its values

#### TLDR
- when dealing with dots, we expect to copy by value; when dealing with arrows, we expect to copy by reference
- good to correctly name classes: `BeastPointer`
- **copy on write** -- when using dot notation (but internally handling stuff using references or pointers), if we're not the only owner of an object but want to modify it, we must copy it first
	- C++ containers behave like this

#### Passing to functions
- **read-only**
	- pass by **value**
	- pass by **const-reference** (for larger stuff)
		- `void f(const std::string & x)`
- **to be modified**
	- pass by **lvalue-reference** (reference without const)
		- `void f(std::string & x)`
		- the argmuent must be something "on the left of the equal sign" - variable, array element,...
	- pass by **rvalue-reference** (reference without const)
		- `void f(std::string && x)`
		- usefull when we can re-use the temporary value instead of dumping it
