brew-dependency
===============

Shows the dependency tree of installed [brew][1] formulae.

```
$:python3 brew-dependency.py
  carthage
  exiftool
  mas
  python
  |  gdbm
  |  openssl
  |  readline
  |  sqlite
  |  |  readline
  |  xz
  qrencode
  |  libpng
  shellcheck
  tldr
  |  libzip
```

Usage
-----
`brew-dependency.py [-h] [-a] [-r] [filter [filter ...]]`

- `-a` or `--all` will display all dependants top-level (e.g., `readline` and `xz`)

- `-r` or `--reverse` shows dependants instead

```
$:python3 brew-dependency.py -r
  carthage
  exiftool
  gdbm
  |  python
  libpng
  |  qrencode
  libzip
  |  tldr
  mas
  openssl
  |  python
  python
  qrencode
  readline
  |  python
  |  sqlite
  shellcheck
  sqlite
  |  python
  tldr
  xz
  |  python
```

- `filter` matches all formulae beginning with that text.

```
$:python3 brew-dependency.py lib qr
  libpng
  libzip
  qrencode
  |  libpng
```


[1]: https://github.com/Homebrew/brew