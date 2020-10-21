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
	- is (at least recently) quite fast (copy/move-elision)
		- without it, the function would be rewritten with a new pointer parameter where to return the value from the function; 
