---
---


### pyenv
installing new versions:
```
> pyenv install -v 3.6.1
```

changing versions (pyenv):
```
> status --is-interactive
> source (pyenv init -|psub)
> pyenv shell 3.7.1
```

### virtualenv
creating (and using) new virtual environments:
```
> virtualenv .venv
> . .venv/bin/activate.fish
```

installing new packages:
```
> pip install ...
```

deactivating:
```
> deactivate
```

### pyqt5
- first, install `sip`; only then `pyqt5`
