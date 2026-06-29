---
date: '2020-03-21'
title: Incrementing and Decrementing Numbers
categoryPart: 1
description: A short post about how to increment/decrement numbers in Vim.
---


Some of you might know that pressing `<C-a>`/`<C-x>` in normal mode _increases/decreases the next number on the line the cursor is currently on_:

```text
There are 12 apples. -<C-a>-> There are 13 apples.
```

But did you also know that it can handle other bases and even alphabetical characters (worked for me but might need to be configured -- see [this wiki article](https://vim.fandom.com/wiki/Increasing_or_decreasing_numbers)):

```text
There are 0b1100 apples. -<C-a>-> There are 0b1101 apples.
There are 0xc apples. -<C-x>-> There are 0xb apples.
This is 'a'. -<C-a>-> This is 'b'.
```

Equipped with this knowledge, one can easily add to and subtract from any number (`10<C-a>`), create a list of numbers in a given base (a relatively simple macro), play around with [caesar ciphers](https://en.wikipedia.org/wiki/Caesar_cipher) and generally do many things that would likely not be possible in other text editors.

