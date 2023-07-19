---
category: "Vim"
category_icon: /assets/category-icons/vim.svg
excerpt: A short post about how history of changes is implemented in Vim.
---

- .
{:toc}

In this post, we'll talk about how history of changes is implemented in Vim (compared to other editors), how to make it persistent, why the `<u>` + `<C-r>` combination isn't doing it justice and what are some plugins you can use to improve your workflow!

### Implementations
Most editors keep a **linear** history of changes made to a given file, meaning that you can only move forward and backward in time. While simple to implement, it isn't an ideal solution -- what if you undoed some changes, made new ones and only after realized that the previous changes were actually the ones you wanted to keep?

This uncommon problem is impossible to deal with using a linear history of changes. Vim, however, offers an elegant solution -- instead of storing changes in a linear manner, it stores them in a **tree**. This means that information about changes made never gets lost (only gets stored in a separate branch) and the problem from the previous paragraph is just a matter of switching from one branch to another.

### Navigating the history
Imagine the following scenario: you're editing a file; you make changes, then undo them, then you make some more changes. The history will look like this (numbers signify the various states of the file after you made changes):

```
      2
     /
0---1---3 (we are here)
```

Using `<u>` and `<C-r>` will move you forward/backward in a linear fashion (meaning that you will only move between states `0`, `1` and `3`). We need more advanced commands to traverse the entire tree.

One way we could do this is based on the **relative time** a given change was made. To move relative to the current time, use the {% ihighlight vim %}earlier{% endihighlight %} and {% ihighlight vim %}later{% endihighlight %} commands:
```vim
:earlier {duration}{unit}
:later   {duration}{unit}
```
where `duration` is an integer and `unit` is `s/h/m/d` for second/hour/minute/day.

You can also use the commands to move based on **chronological order** of the changes made:
```vim
:earlier {num}
:later   {num}
```
will move the file to `num` changes before, based on when they were made. This solves our problem from the previous section, since you can use {% ihighlight vim %}earlier{% endihighlight %} (possibly repeatedly) to switch back to the branch that you decided was actually the one you wanted to keep.

Last way to use the commands is to move based on **writes to file**:
```vim
:earlier {num}f
:later   {num}f
```
will change the state of the file to `num` writes to file before.

### Persistent history
When working frequently on the same files for a prolonged period of time, it can be quite useful to make the history of changes persistent, so that closing the file won't discard the history of changes. Luckily, Vim has you covered -- you can enable persistent history by adding `set undofile` to your `.vimrc`.

The {% ihighlight vim %}<`.>{% endihighlight %} command is nice, as it takes you back to the line that was last changed. You can also just `<u>` and `<C-r>` (like I do, although I shouldn't), but the former is far more elegant 🙂.

### Plugins
If the commands and techniques mentioned above weren't enough for you, there are a number of plugins that make it easy to view and traverse the graph. I've personally used [UndoTree](https://github.com/mbbill/undotree) and found it quite nice, but there are other alternatives (like [Mundo](https://github.com/simnalamburt/vim-mundo), for example). Give them a try and see for yourself!

### Additional resources
- [Undo and Redo](https://vim.fandom.com/wiki/Undo_and_Redo) and [Using undo branches](https://vim.fandom.com/wiki/Using_undo_branches) from Vim Wikipedia.
- Vim's built-in documentation (invoke using {% ihighlight vim %}:help {something}{% endihighlight %})
