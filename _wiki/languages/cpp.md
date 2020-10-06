---
title: C++
---

### Dictionaries
- `#include <map>`            // hashing, constant access
- `#include <unordered_map>`  // R&B trees, log(n) access

| Action   | Code                  |
| ---      | ---                   |
| create   | `map<int, int> m;`    |
| contains | `m.count(element);`   |
| add      | `m[index] = element;` |

### Strings

| Action | Code          |
| ---    | ---           |
| length | `s.length();` |

### Array 

| Action          | Code                                                   |
| ---             | ---                                                    |
| create          | `int *array = new int[size];`, requires `<new>`        |
| fill with stuff | `fill_n(array, size, element)`, requires `<algorithm>` |

### Sorting
- `#include <algorithm>`
- `std::sort(RandomAccessIterator first, RandomAccessIterator last, Compare comp)`
	- `comp` not required, default used
	- usually `vector.begin()` and `vector.end()`
