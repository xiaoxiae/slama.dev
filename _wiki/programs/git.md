---
---

### Basic operations
- `git add <file>` -- stage a file
	- `-p` -- stages a file by hunks
		- `s` -- split into smaller hunks
	- `-f` -- add otherwise ignored file

- `git commit` -- issues a commit
	- `--amend` -- amends to the previous commit
	- `-m <message>` -- with a certain message

- `git push` -- pushes the changes to a remote
	- `-u <remote> <branch>` -- sets the upstream, making the pull argument-less
	- `-f` -- force push

### Tracking changes
- `git status` -- show the status of the working tree

- `git log` -- lists the commit log
	- `--decorate --all --graph` -- make a nice graph

- `git diff` -- see differences
	- `<file>` -- of a specific file
	- `<remote>` -- local vs remote
	- `--cached` -- see staged differences
	- `-b` -- not including whitespace diffs

### Branches
- `git branch` -- list all branches
	- `<name>` -- create a new branch
	- `-d <name>` -- delete a branch
		- `git push <remote> :the_branch` -- delete on the remote

- `git checkout <branch>` -- switches head to the specified branch

- `git merge <branch>` -- attempts to automatically merge the specified branch onto the current branch
	- `git mergetool --tool=vimdiff` -- performs manual merge
		- `:diffg RE` -- remote (right)
		- `:diffg BA` -- base (center)
		- `:diffg LO` -- local (left)

- `git rebase` -- apply commits from one branch on top of another
	- useful for keeping the history linear

### Remotes
- `git remote`
	- `add <name> <url>` -- add a remote from a URL
	- `show` -- show remtotes
	- `-v` -- verbose (URLs)
	- `-d <name> <branch>` -- remove branch on remote
- `git pull` -- pull the chaadressesnges from the remote
	- if upstream is set, no additional arguments are needed

### Resetting files
- `git reset` -- reset stuff!
	- `HEAD -- <file>` -- remove file from staging area
	- `--soft HEAD~1` -- move head a commit back
- `git checkout HEAD -- <file>` -- reset file changes
- `git restore`

### Other
- `git cherrypick <commit>` -- apply a specified commit on the current branch
	- `<start^..end>` -- apply a range of commits including start
- `git stash` -- store unstaged changes to be used later
	- `pop` -- pop the stashed changes
	- `drop` -- drop the latest stash
	- `--all` -- includes untracked files
- `git bisect` -- performs a binary selection on the branch
	- `start` -- starts the bisection
	- `good` -- label a commit "good"
	- `bad` -- label a commit "bad"
	- TODO: add bisect reset
