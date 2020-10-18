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

{% match #### Dictionaries  %}
- we can implement one as a list of tuples (**association lists**)
- `Data.Map` has a faster implementation (**maps**)
	- better to import as `Map`, because some of the methods clash

| Function                                                    | Behavior                                    |
| ---                                                         | ---                                         |
| `fromList :: (Ord k) => [(k, v)] -> Map.Map k v`            | takes an association list and returns a map |
| `lookup :: (Ord k) => k -> Map.Map k v -> Maybe v`          | (maybe) get an element from the map         |
| `insert :: (Ord k) => k -> v -> Map.Map k v -> Map.Map k v` | insert an element to the map                |
| `size :: Map.Map k v -> Int`                                | return the size of the dictionary           |

{% match ### Operators %}
- _they are also functions, but any function compromised of only special characters is infix by default, wink wink_

{% match ### Other %}

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

#### Pattern matching
- normal use:

```hs
factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial(n - 1)
```

- lists:

```hs
head' :: [a] -> a
head' []    = error "Can't head an empty list."
head' (x:_) = x
```

##### As-patterns
- when we also want the original pattern match:

```hs
firstLetter :: String -> String
firstLetter [] = "The string is empty!"
firstLetter all@(x:_) = "The first character of '" ++ all ++ "'is '" ++ [x]
```

#### Guards
- conditions on a given pattern

```hs
bmiTell :: Double -> String
bmiTell bm
  | bm <= 18.5 = "Skinny"
  | bm <= 20.0 = "Ok."
  | bm <= 30.0 = "Not skinny."
  | otherwise  = "See a doctor."
```

#### `where`
- defining stuff locally to make the code more readable

```hs
bmiTell :: Double -> Double -> String
bmiTell weight height
  | bmi <= skinny = "Skinny"
  | bmi <= normal = "Ok."
  | bmi <= overweight = "Not skinny."
  | otherwise  = "See a doctor."
  where bmi = weight / height^2
        skinny = 18.5
        normal = 20.0
        overweight = 30.0
```

- seen only within a body where they are defined
	- not even shared across bodies for different patters
- both functions and variables can be defined inside `where`
- we can also pattern match inside:

```hs
  where bmi = weight / height^2
        (skinny, normal, overweight) = (18.5, 20.0 30.0)
```
```hs
  where (f:_) = firstName
        (l:_) = lastName
```

#### `let ... in` expressions
- like guards, but much more local

```hs
testFunction :: Int -> Int
testFunction f =
    let x = 3
        y = 5
    in f * x + y
```
- pattern matching can also be used
- also, they are expressions, so we can use them anywhere

#### `case` expressions
- pattern matching anywhere in the code (since it's just syntactic sugar for case expressions!)

```hs
let head' :: [a] -> a;
    head' xs = case xs of [ ]    -> error "No head for empty lists!"
                          (x: _) -> x
```

#### Sections
- partially apply infix functions

```hs
divideByTen :: (Floating a) => a -> a
divideByTen = (/10)
--same as divideByTen x = x/10

overTen :: (Floating a) => a -> a
overTen = (10/)
--same as overTen x = 10/x

divide :: (Floating a) => a -> a -> a
divide = (/)
--same as divide a b = a/b
```
- watch out for `(-4)` -- this is actually just `-4` -- do `subtract 4` instead

#### Higher-order functions
- the concept of partially applying parameters to functions:
	- `zip [1, 2, 3]` is a `Num a => [b] -> [(a, b)]` type function
	- `(+3)` is a `Num a => a -> a` type function
- generally, `f a = g b a` is the same as `f = g b` (because of this)
- parentheses in type declarations matter (since `->` is right-associative):

```hs
applyTwice :: (a -> a) -> a -> a
applyTwice f a = f (f a)
```

```hs
zipWith' :: (a -> b -> c) -> [a] -> [b] -> [c]
zipWith' f _ []          = []
zipWith' f [] _          = []
zipWith' f (x:xs) (y:ys) = f x y:zipWith' f xs ys
```

| Function                               | Behavior                              |
| ---                                    | ---                                   |
| `map :: (a -> b) -> [a] -> [b] `       | maps a function onto a list           |
| `filter :: (a -> Bool) -> [a] -> [a] ` | filters out elements that don't match |


#### Lambdas
- one-time functions

```hs
filter (\x -> x `mod` 3 == 0) [1..100]
```

#### Folding
- take a binary function, a variable and start 'folding' a given list (foldable, actually, but I'm not sure what that is for now) by applying the binary function between the accumulator and the head of the list

| Function                                   | Behavior                          |
| ---                                        | ---                               |
| `foldl :: (b -> a -> b) -> b -> [a] -> b`  | left-to-right                     |
| `foldr :: (a -> b -> b) -> b -> [a] -> b`  | right-to-left (note the `a -> b`) |
| `foldl1 :: (a -> a -> a) -> [a] -> a`      | `foldl`, 1st element is the acc.  |
| `foldr1 :: (a -> a -> a) -> [a] -> a`      | `foldr`, ^                        |
| `foldl' :: (b -> a -> b) -> b -> [a] -> b` | non-lazy; found in `Data.List`    |
| `foldr' :: (b -> a -> b) -> b -> [a] -> b` | ^                                 |
| `foldl1' :: (a -> a -> a) -> [a] -> a`     | ^                                 |
| `foldr1' :: (a -> a -> a) -> [a] -> a`     | ^                                 |

- list can be the accumulator too (it doesn't just have to be like an int):

```hs
map' :: (a -> b) -> [a] -> [b]
map' f = foldr (\x acc -> f x : acc) []
```

#### Function Application (`$`)
```hs
($) :: (a -> b) -> a -> b
f $ x = f x
```
- looks useless, but changes precedence
- when used, everything on the right is applied as a parameter to what is on the left:

```hs
sum (map sqrt [1..100])
sum $ map sqrt [1..100]

sqrt (1 + 2 + 3)
sqrt $ 1 + 2 + 3

sum (filter (> 10) (map (*2) [2..10]))
sum $ filter (> 10) (map (*2) [2..10])
sum $ filter (> 10) $ map (*2) [2..10]
```

#### Function Composition `(.)`
```hs
(.) :: (b -> c) -> (a -> b) -> a -> c
f . g = \x f (g x)
```
- is right-associative (`f (g (z x)) == (f . g . z) x`)
- is sometimes more concise than a lambda

```hs
\x -> negate (abs x)
negate . abs
```

### Modules
- **module** = a file that defines some functions, types and type classes
- **program** = a collection of modules

#### Importing
- must be done before defining any functions

```hs
import Module1                  -- entire module
import Module2 (f1, f2)         -- only specific functions
import Module2 hiding (f1, f2)  -- except specific functions
import qualified Module2        -- must be called with Module2.something
import qualified Module2 as M   -- must be called with M.something
```

#### Creating
- soubor `Geometry.hs`

```hs
module Geometry
( sphereVolume
, sphereArea
, cubeVolume
) where

<function definitions>
```

##### Submodules
- folder `Geometry`
- file `Sphere.hs`

```hs
module Geometry.Sphere
( volume
, area
, cubeVolume
) where

<function definitions>
```

---

### Resources
- [Learn You a Haskell for Great Good!](http://learnyouahaskell.com/introduction#about-this-tutorial)
- Kowainik's [Haskell style guide](https://kowainik.github.io/posts/2019-02-06-style-guide)
- [Ormolu autoformatter](https://github.com/tweag/ormolu)

