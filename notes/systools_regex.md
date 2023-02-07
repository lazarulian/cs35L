# System Commands & RegEx

## Table of Contents

- [System Commands \& RegEx](#system-commands--regex)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Grep](#grep)
  - [Regular Expressions](#regular-expressions)
    - [Basic Regular Expressions](#basic-regular-expressions)
    - [Quoting](#quoting)
    - [Extended Regular Expressions](#extended-regular-expressions)
    - [Examples](#examples)
  - [ps (processes)](#ps-processes)
  - [chmod (permissions)](#chmod-permissions)
  - [wc (word count)](#wc-word-count)

## Introduction

---

When using the system and especially the abstractions of the shell, we do not want to hard code all of the small programs that we can use into the shell. That would make maintaining and adding programs difficult. Thus, in the usr/bin in path, we have a ton of small tools of the system that accomplish tasks really well. The components are then connected to make them fast, maintainable and well structured.

&nbsp;
&nbsp;
&nbsp;

## Grep

---

If `grep` finds a line with the PATTERN, it outputs it. So it is similar to cat, but more selective. In fact, if you use a pattern that matches every character, grep can behave identically to cat: `grep '.*' filename`

```shell
NAME
       grep, egrep, fgrep, rgrep - print lines that match patterns

SYNOPSIS
       grep [OPTION...] PATTERNS [FILE...]
       grep [OPTION...] -e PATTERNS ... [FILE...]
       grep [OPTION...] -f PATTERN_FILE ... [FILE...]

DESCRIPTION
       grep  searches  for  PATTERNS  in  each  FILE.  PATTERNS is one or more
       patterns separated by newline characters, and  grep  prints  each  line
       that  matches a pattern.  Typically PATTERNS should be quoted when grep
       is used in a shell command.

       A FILE of “-”  stands  for  standard  input.   If  no  FILE  is  given,
       recursive  searches  examine  the  working  directory, and nonrecursive
       searches read standard input.

       In addition, the variant programs egrep, fgrep and rgrep are  the  same
       as  grep -E,  grep -F,  and  grep -r, respectively.  These variants are
       deprecated, but are provided for backward compatibility.

OPTIONS
   Pattern Syntax
       -E, --extended-regexp
              Interpret PATTERNS as extended regular  expressions  (EREs,  see
              below).

   Matching Control
       -e PATTERNS, --regexp=PATTERNS
              Use  PATTERNS  as the patterns.  If this option is used multiple
              times or is combined with the -f (--file) option, search for all
              patterns  given.   This  option can be used to protect a pattern
              beginning with “-”.

       -f FILE, --file=FILE
              Obtain patterns from FILE, one per line.  If this option is used
              multiple  times  or  is  combined with the -e (--regexp) option,
              search for all patterns given.  The  empty  file  contains  zero
              patterns, and therefore matches nothing.
```

&nbsp;
&nbsp;
&nbsp;

## Regular Expressions

### Basic Regular Expressions

---

grep actually uses Basic regular expressions (BREs), a simpler form of the more familiar regex, extended regular expressions (EREs). It also only matches against single lines at a time.

- `[]` matches a single character but only those that are included in the set enclosed in the square brackets
- `^` matches the start of a the line
- `$` matches the end of the line
- `.` matches every single character
- `*` globbing pattern that needs to be enclosed in quotes, must be escaped otherwise
- `\` must be escaped

### Quoting

---

- the idea that you feed the output of programs as quoted programs to other programs as their inputs
  - Quoting and little language commands like grep go hand-in-hand. Scripts are evaluated by the shell first before being shipped off as arguments to its child programs, so make sure you quote and/or escape everything keeping in mind how your initial string will be resolved as it makes its way through each program.
- As described in single quoting, single quotes are often used for grep expressions because they preserve everything literally - what you see within the quotes is exactly what you're giving grep.
- double quotes to be able to interpolate regex fragments into the larger expression.
  - we use double backslashes \\ since \ is still a special character within double quotes which much be escaped to represent themselves by the time it reaches grep.

### Extended Regular Expressions

---

Historically there was another team that came up with alternate syntax to the familiar grep, called egrep. Nowadays you can use the -E flag to specify that the pattern is using the extended syntax instead:

- `+` quantifier to watch 1 or more occurences, similar to PP\*
- `#{2-5}` would match `#` 2-5 times in a row inclusive. We must quote otherwise it will glob in the shell
- `(eggert|foo)` matches either the entire string eggert or the entire string foo
- `[^a-z]` negates the values from the response, removes lines with just a-z responses
- ``

### Examples

---

```bash
[a-z]       # matches any character that matches in the range of a-z
[]a-z]      # matches either the closing bracket or characters from a-z (must be in quotes)
[^a-z]      # matches all non a-z lines as the ^ acts as a negation of the set
[a-z^]      # matches either a-z or ^
[a-z*]      # matches a-z or star
abc*d       # abcd or abccd or abcccd
\(abc\)*d   # abcd or abcabcd or abcabcabcd
P{3,5}      # 3-5 instances of p
P{3;}       # 3 to infinity instances of P
(###|Eggert)    # matches either ### or Eggert
^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])$ # find numbers between 0-255
\[\’\”\\\]      # [’”\]
\['\''"'\']     #  [’”\]
['\''"'\']      # would fail, as it does not evaluate the set rather the expression literal [\"']
'[a-zA-Z0-9]+'          # at least 1 alphanumeric character
'\\"([^"\]|\\.)*\\"'    # \"(something)\", where (something) is . OR neither " or \
```

&nbsp;
&nbsp;
&nbsp;

## ps (processes)

---

```bash
ps -efH
```

- `e` selects all processes
- `f` full format listing
- `H` shows process hierarchy

&nbsp;
&nbsp;
&nbsp;

## chmod (permissions)

---

- can take arguments in either octal or alphanumeric form
- you can `add +`, `delete -`, or `set =`

```bash
NAME
       chmod - change file mode bits

SYNOPSIS
       chmod [OPTION]... MODE[,MODE]... FILE...
       chmod [OPTION]... OCTAL-MODE FILE...

OCTAL NOTATION

Execute - 1
Read    - 4
Write   - 2
```

- `chmod 755 readme.md` would give RWX-RX-RX
- `chmod 655 readme.md` would give RW-RX-RX
- `chmod 7-5-1 readme.md` would give RWX-RX-X
- `chmod a+x,u-r file1.txt file2.py` would give X-R-

&nbsp;
&nbsp;
&nbsp;

## wc (word count)

---

```bash
NAME
       wc - print newline, word, and byte counts for each file

SYNOPSIS
       wc [OPTION]... [FILE]...
       wc [OPTION]... --files0-from=F

DESCRIPTION
       Print  newline,  word, and byte counts for each FILE, and a total line if
       more than one FILE is specified.  A word is a non-zero-length sequence of
       characters delimited by white space.

       With no FILE, or when FILE is -, read standard input.

       The  options below may be used to select which counts are printed, always
       in the following order: newline,  word,  character,  byte,  maximum  line
       length.

       -c, --bytes
              print the byte counts

       -m, --chars
              print the character counts

       -l, --lines
              print the newline counts

       -w, --words
              print the word counts
```

&nbsp;
&nbsp;
&nbsp;
