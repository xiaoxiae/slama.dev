---
---

Here is a [quine](https://en.wikipedia.org/wiki/Quine_%28computing%29) that I recently stumbled upon when playing around with Python. It is likely a „cheating“ quine, due to the fact that I'm using interpreter messages (hence the title of this short post), but I found it quite interesting anyway.

Here it is, saved as a file called `a`:

```py
  File "a", line 1
    File "a", line 1
    ^
IndentationError: unexpected indent
```

---

Interestingly, it seems that Python `3.9` introduced absolute paths to the source file and changed the format a bit, so the quine would have to be adjusted like so:

```py
  File "path/to/a", line 1
    File "path/to/a", line 1
IndentationError: unexpected indent
```

Not as cool as before 😢.

