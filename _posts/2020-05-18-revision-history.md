---
layout: post
category: "Vim"
---

In this second post about Vim, we'll be looking at how to more efficiently work with changes made to a given file...

---

As most people who use Vim know, you can easily undo (`<u>`) and redo (`<C-r`) changes made to a given file (buffer, actually). But what you might not know is that there are other, more advanced features, that allow ....

---

### History of changes
Most editors keep a **linear** history of changes made to a given file, meaning that you can only move forward and backward, nothing more. While simple to implement, it isn't an ideal solution -- what if you undoed some changes, made new ones and only after realized that the previous changes were actually the ones you wanted to keep?

This is not an uncommon problem (at least to me, when exploring various ways to implement a certain feature) that is nigh impossible to deal with using a linear history of changes.  Vim, however, offers an elegant solution -- instead of storing changes in a linear manner, it stores them in a **tree**. This means that information about changes made never gets lost (only gets stored in a separate branch) and the problem from the previous paragraph can easily be resolved by switching from one branch to another.

... 

### Persistent undo
When working on files for a prolonged period of time, it can be CONTINUING WORK tedious to manually look for the last place  would be quite convenient to open the file and start working where continue wherever the last position.bbb

Luckily, Vim has you covered -- you can enable saving the file history by adding the following line to your `.vimrc` file:

```
:set undofile
```

That way when opening the file, you can undo/redo like the file was never closed. The `\`.` command is quite handy, as it allows you to jump back to the line that was last changed.

### Additional resources
- [Undo and Redo](https://vim.fandom.com/wiki/Undo_and_Redo) and  [Using undo branches](https://vim.fandom.com/wiki/Using_undo_branches) from Vim Wikipedia.

