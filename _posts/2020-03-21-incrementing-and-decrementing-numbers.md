---
category: "Vim"
---

Some of you might know that pressing `<C-a>`/`<C-x>` in command mode _increases/decreases the next number on the line the cursor is currently on_:

```
There is 12 apples. -<C-a>-> There is 13 apples.
```

But did you also know that it can handle other bases and even alphabetical characters (worked for me but might need to be configured -- see [this wiki article](https://vim.fandom.com/wiki/Increasing_or_decreasing_numbers)):

```
There is 0b1100 apples. -<C-a>-> There is 0b1101 apples.
There is 0xc apples. -<C-x>-> There is 0xb apples.
This is 'a'. -<C-a>-> This is 'b'.
```

Equipped with this knowledge, one can easily add to and subtract from any number (`10<C-a>`), create a list of numbers in a given base (a relatively simple macro), play around with [caesar cypers](https://en.wikipedia.org/wiki/Caesar_cipher) and generally do many things that would likely not be possible in other text editors.

