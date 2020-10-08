---
---

{% match ### Control flow %}

{% match #### If/else %}
- is an expression
- `if <condition> then <if true> else <if false>`
- `else` is mandatory -- what would that even mean?

{% match ### Data structures %}

{% match #### Lists %}
- **homogenous** (can only hold an item of a certain type)
- strings are lists of chars
- lists of lists are fine, but they still have the same type

| Operator   | Behavior                                                            |
| ---        | ---                                                                 |
| `l1 ++ l2` | join                                                                |
| `e: l`     | put at the beginning                                                |
| `l !! n`   | get {% latex %}n{% endlatex %}-th element                           |
| `l1 < l2`  | compare lexicographically; works for other comparison operators too |

| Function    | Behavior                                       |
| ---         | ---                                            |
| `head`      | get first element                              |
| `tail`      | get elements except first                      |
| `last`      | get last element                               |
| `tail`      | get elements except last                       |
| `length`    | number of elements                             |
| `null`      | is empty?                                      |
| `reverse`   | reverse list                                   |
| `take n`    | take first {% latex %}n{% endlatex %} elements |
| `drop n`    | drop first {% latex %}n{% endlatex %} elements |
| `elem e`    | is element in list?                            |
| `cycle`     | repeat list forever                            |
| `zip l`     | zip the list with another one                  |

{% match #### Ranges %}
- `[1..20]`, `[a..z]`... anything that can be enumerated
- `[first..]`, `[first,second..]`, `[first..last]`, `[first,second..last]`
	- see [this StackOverflow post](https://stackoverflow.com/questions/7958181/ranges-in-haskell-ghci#7958408) that describes the behavior

{% match #### List comprehensions %}
- `[x | x <- [1..10], mod x 2 == 1]`
- can contain multiple `variable <- stuff` and conditions, in pretty much any order (so far as I can tell)
- they can be nested

{% match #### Tuples %}
- **not homogenous**
- the size is fixed
- denoted with parentheses
- better for things like vectors:
	- `[(1, 2), (1, 2, 3), (3, 1)]` wouldn't compile

| Function  | Behavior                                       |
| ---       | ---                                            |
| `fst`     | get first element (only for pairs!)            |
| `snd`     | get second element (only for pairs!)           |

{% match ### Operators %}
- _they are also functions, but any function compromised of only special characters is infix by default, wink wink_

#### Comparables

| Operator   | Behavior       |
| ---        | ---            |
| `==`       | equals         |
| `/=`       | does not equal |
| `>=`, `<=` | le, ge         |
| `>`, `<`   | lt, gt         |

| Operator | Behavior |
| ---      | ---      |
| `not`    | negation |
| `&&`, `||` | and, or   |

{% match ### Functions %}
- defined using `function p1 p2 = <body>`
- can't begin with a capital letter!
- good practice to give it an explicit type declaration:
```hs
removeNonUppercase :: String -> String
removeNonUppercase st = [ c | c <- st, c `elem` ['A'..'Z']]
```

#### Calling
- `function p1 p2 p3`

{% match ### Types %}
- Haskell has **type inference**
	- can infer the variable from its value

{% match #### Common types %}

| Type      | Meaning                     |
| ---       | ---                         |
| `Int`     | whole numbers               |
| `Integer` | arbitrary precision integer |
| `Float`   | single precision float      |
| `Double`  | double precision float      |
| `Bool`    | boolean                     |
| `Char`    | single char                 |

#### Class constraints
- `:t 123` gives `Num p => p`, `Num p` is a **class constraint``
	- means that `p` must be a member of the `Num` class
- note that `read "1"` will crash, since `:t read` is `Read a => String -> a` -- Haskell doesn't know, what to do with the result
	- it has to
	- can be fixed with `:: Type` -- `read "1" :: Int`)
- `fromIntegral :: (Integral a, Num b) => a -> b` is quite useful for converting a number into a more general number

| Constraint  | Meaning                                         |
| ---         | ---                                             |
| `Eq`        | testing for equality                            |
| `Ord`       | have an ordering                                |
| `Show`      | can be represented as strings                   |
| `Read`      | can be converted from strings                   |
| `Enumerate` | are sequentially ordered (can be enumerated)    |
| `Bounded`   | have an upper and lower bound                   |
| `Num`       | acts like a number                              |
| `Integral`  | only whole numbers, contains `Int` and `Integer |
| `Floating`  | floating point numbers (`Float` and `Double`)   |

---

### Resources
- [Learn You a Haskell for Great Good!](http://learnyouahaskell.com/introduction#about-this-tutorial)

