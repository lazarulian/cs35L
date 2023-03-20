# Bash Implementation

## Table of Contents

- [Bash Implementation](#bash-implementation)
  - [Table of Contents](#table-of-contents)
  - [Setting Path Variables](#setting-path-variables)
  - [patch](#patch)
  - [tr (replace)](#tr-replace)
  - [ps (processes)](#ps-processes)
  - [chmod (permissions)](#chmod-permissions)
  - [wc (word count)](#wc-word-count)
  - [Which](#which)
  - [Sleep](#sleep)
  - [Sed](#sed)
  - [SEQ](#seq)
  - [LN](#ln)
  - [LS](#ls)

## Setting Path Variables

- `export:` This command makes the variable available to child processes.
- `PATH=:` This sets the value of the PATH variable to an empty string.
- `$PATH::` This appends the current value of the PATH variable to the new value, with a colon separator. This ensures that any existing directories in the PATH are not lost.

So, the command export `PATH=$PATH:/new/directory` adds /new/directory to the end of the PATH list, so that the shell will look for executables in this directory as well. This is useful when you have installed a new program that is not in the default system path.

```
Export PATH=/Desktop/new_cat:$PATH
```

- where new_cat has the new cat declaration

## patch

```bash
PATCH
NAME patch - apply a diff file to an original
SYNOPSIS patch [options] [originalfile [patchfile]]
        -d dir  or  --directory=dir
        -i patchfile  or  --input=patchfile
        -o outfile  or  --output=outfile
```

## tr (replace)

```bash
# Shift by 12 characters(A becomes M, and vice versa)
echo ABCDE | tr '[A-Z]' '[M-ZA-L]'
# Turns Back
echo MNOPQ | tr '[M-ZA-L]' '[A-Z]'

# Shift by 3 characters(A becomes D, and vice versa)
echo ABCDE | tr '[A-Z]' '[M-ZABC]'
# Turns Back
echo MNOPQ | tr '[M-ZABC]' '[A-Z]'
```

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

Print  newline,  word, and byte counts for each FILE, and a total line if more than one FILE is specified. A word is a non-zero-length sequence of characters delimited by white space.

With no FILE, or when FILE is -, read standard input.

The options below may be used to select which counts are printed, always in the following order: newline,  word,  character,  byte,  maximum  line length.

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

## Which

```bash
Which (1)

NAME
       which - shows the full path of (shell) commands.

SYNOPSIS
       which [options] [--] programname [...]
```

&nbsp;
&nbsp;
&nbsp;

## Sleep

```bash
NAME
    sleep - delay for a specified amount of time

SYNOPSIS
    sleep NUMBER[SUFFIX]...
    sleep OPTION

DESCRIPTION

Pause  for NUMBER seconds.  SUFFIX may be 's' for seconds (the default), 'm' for minutes, 'h' for hours or 'd' for days.  NUMBER need not be an integer.  Given two or more arguments, pause for the amount of time specified by the sum of their values.
```

&nbsp;
&nbsp;
&nbsp;

## Sed

```bash
NAME
    sed - stream editor for filtering and transforming text

SYNOPSIS
    sed [OPTION]... {script-only-if-no-other-script} [input-file]...

DESCRIPTION

Sed  is  a stream editor.  A stream editor is used to perform basic text transformations on an input stream (a file or input from a pipeline).  While in some ways similar to an editor which permits scripted edits. sed works by making only one pass over the input(s), and is consequently more efficient.  But it is seds ability to filter text in a pipeline which particularly distinguishes it from other types of editors.

-n, --quiet, --silent
    suppress automatic printing of pattern space

-e script, --expression=script
    add the script to the commands to be executed

-f script-file, --file=script-file
    add the contents of script-file to the commands to be executed

--follow-symlinks
    follow symlinks when processing in place

-i[SUFFIX], --in-place[=SUFFIX]
    edit files in place (makes backup if SUFFIX supplied)

-l N, --line-length=N
    specify the desired line-wrap length for the l command

--posix
    disable all GNU extensions.

-E, -r, --regexp-extended
    use extended regular expressions in the script (for portability use POSIX -E).

-s, --separate
    consider files as separate rather than as a single, continuous long stream.

--sandbox
    operate in sandbox mode (disable e/r/w commands).
```

&nbsp;
&nbsp;
&nbsp;

## SEQ

```bash
NAME
       seq - print a sequence of numbers

SYNOPSIS
       seq [OPTION]... LAST
       seq [OPTION]... FIRST LAST
       seq [OPTION]... FIRST INCREMENT LAST

DESCRIPTION

Print numbers from FIRST to LAST, in steps of INCREMENT. Mandatory arguments to long options are mandatory for short options too.

    -f, --format=FORMAT
        use printf style floating-point FORMAT

    -s, --separator=STRING
        use STRING to separate numbers (default: \n)

    -w, --equal-width
        equalize width by padding with leading zeroes

If  FIRST or INCREMENT is omitted, it defaults to 1.  That is, an omitted INCREMENT defaults to 1 even when LAST is smaller than FIRST.  The sequence of numbers ends when the sum of the current number and INCREMENT would become greater than LAST.  FIRST, INCREMENT, and LAST are interpreted as floating point values.  INCREMENT is usually positive if FIRST is smaller than LAST, and INCREMENT is usually negative  if FIRST  is  greater  than LAST.   INCREMENT  must not be 0; none of FIRST, INCREMENT and LAST may be NaN. FORMAT must be suitable for printing one argument of type 'double'; it defaults to %.PRECf if FIRST, INCREMENT, and LAST are all fixed point decimal numbers with maximum precision PREC, and to %g otherwise.
```

&nbsp;
&nbsp;
&nbsp;

## LN

```bash
NAME
       ln - make links between files

SYNOPSIS
       ln [OPTION]... [-T] TARGET LINK_NAME
       ln [OPTION]... TARGET
       ln [OPTION]... TARGET... DIRECTORY
       ln [OPTION]... -t DIRECTORY TARGET...

DESCRIPTION

In the 1st form, create a link to TARGET with the name LINK_NAME.  In the 2nd form, create a link to TARGET in the current directory.  In the 3rd and 4th forms, create links to each TARGET in DIRECTORY.  Create hard links by default, symbolic links with --symbolic.  By default, each destination (name of new link) should not already exist.  When creating hard links, each TARGET must exist.  Symbolic links can hold arbitrary text; if later resolved, a relative link is interpreted in relation to its parent directory.

Mandatory arguments to long options are mandatory for short options too.

    --backup[=CONTROL]
        make a backup of each existing destination file

    -b     like --backup but does not accept an argument

    -d, -F, --directory
        allow the superuser to attempt to hard link directories

    -f, --force
        remove existing destination files

    -i, --interactive
        prompt whether to remove destinations

    -L, --logical
        dereference TARGETs that are symbolic links

    -n, --no-dereference
        treat LINK_NAME as a normal file if it is a symbolic link to a directory

    -P, --physical
        make hard links directly to symbolic links

    -r, --relative
        with -s, create links relative to link location

    -s, --symbolic
        make symbolic links instead of hard links

    -S, --suffix=SUFFIX
        override the usual backup suffix

    -t, --target-directory=DIRECTORY
        specify the DIRECTORY in which to create the links

    -T, --no-target-directory
        treat LINK_NAME as a normal file always

    -v, --verbose
        print name of each linked file
```

&nbsp;
&nbsp;
&nbsp;

## LS

```bash
NAME
       ls - list directory contents

SYNOPSIS
       ls [OPTION]... [FILE]...

DESCRIPTION

List information about the FILEs (the current directory by default).  Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

Mandatory arguments to long options are mandatory for short options too.

    -a, --all
            do not ignore entries starting with .

    -A, --almost-all
            do not list implied . and ..

    --author
            with -l, print the author of each file

    -b, --escape
            print C-style escapes for nongraphic characters

    --block-size=SIZE
    with -l, scale sizes by SIZE when printing them; e.g., '--block-size=M'; see SIZE format below

    -B, --ignore-backups
            do not list implied entries ending with ~

    -c     with -lt: sort by, and show, ctime (time of last modification of file status information); with -l: show ctime and sort by name; otherwise: sort by ctime, newest first

    -C     list entries by columns

    --color[=WHEN]
            color the output WHEN; more info below

    -d, --directory
            list directories themselves, not their contents

    -D, --dired
            generate output designed for Emacs' dired mode

    -f     list all entries in directory order

    -F, --classify[=WHEN]
            append indicator (one of */=>@|) to entries WHEN

    --file-type
            likewise, except do not append '*'

    --format=WORD
            across -x, commas -m, horizontal -x, long -l, single-column -1, verbose -l, vertical -C

    --full-time
            like -l --time-style=full-iso

    -g     like -l, but do not list owner

    --group-directories-first
            group directories before files; can be augmented with a --sort option, but any use of --sort=none (-U) disables grouping

    -G, --no-group
            in a long listing, don't print group names

    -h, --human-readable
            with -l and -s, print sizes like 1K 234M 2G etc.

    --si   likewise, but use powers of 1000 not 1024

    -H, --dereference-command-line
            follow symbolic links listed on the command line

    --dereference-command-line-symlink-to-dir
            follow each command line symbolic link that points to a directory

    --hide=PATTERN
            do not list implied entries matching shell PATTERN (overridden by -a or -A)

    --hyperlink[=WHEN]
            hyperlink file names WHEN

    --indicator-style=WORD
            append indicator with style WORD to entry names: none (default), slash (-p), file-type (--file-type), classify (-F)

    -i, --inode
            print the index number of each file

    -I, --ignore=PATTERN
            do not list implied entries matching shell PATTERN

    -k, --kibibytes
            default to 1024-byte blocks for file system usage; used only with -s and per directory totals

    -l     use a long listing format

    -L, --dereference
            when showing file information for a symbolic link, show information for the file the link references rather than for the link itself

    -m     fill width with a comma separated list of entries

    -n, --numeric-uid-gid
            like -l, but list numeric user and group IDs

    -N, --literal
            print entry names without quoting

    -o     like -l, but do not list group information

    -p, --indicator-style=slash
            append / indicator to directories

    -q, --hide-control-chars
            print ? instead of nongraphic characters

    --show-control-chars
            show nongraphic characters as-is (the default, unless program is 'ls' and output is a terminal)

    -Q, --quote-name
            enclose entry names in double quotes

    --quoting-style=WORD
            use quoting style WORD for entry names: literal, locale, shell, shell-always, shell-escape, shell-escape-always, c, escape (overrides QUOTING_STYLE environment variable)

    -r, --reverse
            reverse order while sorting

    -R, --recursive
            list subdirectories recursively

    -s, --size
            print the allocated size of each file, in blocks

    -S     sort by file size, largest first

    --sort=WORD
            sort by WORD instead of name: none (-U), size (-S), time (-t), version (-v), extension (-X), width

    --time=WORD
            change the default of using modification times; access time (-u): atime, access, use; change time (-c): ctime, status; birth time: birth, creation;

            with -l, WORD determines which time to show; with --sort=time, sort by WORD (newest first)

    --time-style=TIME_STYLE
            time/date format with -l; see TIME_STYLE below

    -t     sort by time, newest first; see --time

    -T, --tabsize=COLS
            assume tab stops at each COLS instead of 8

    -u     with -lt: sort by, and show, access time; with -l: show access time and sort by name; otherwise: sort by access time, newest first

    -U     do not sort; list entries in directory order

    -v     natural sort of (version) numbers within text

    -w, --width=COLS
            set output width to COLS.  0 means no limit

    -x     list entries by lines instead of by columns

    -X     sort alphabetically by entry extension

    -Z, --context
            print any security context of each file

    --zero end each output line with NUL, not newline

    -1     list one file per line
```
