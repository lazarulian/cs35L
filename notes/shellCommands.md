# Shell Commands

## Table of Contents

- [Shell Commands](#shell-commands)
  - [Table of Contents](#table-of-contents)
  - [General Commands](#general-commands)
    - [Basic Output Manipulation](#basic-output-manipulation)
    - [Path \& the Shell](#path--the-shell)
    - [Command Arguments](#command-arguments)
  - [Running Multiple Commands](#running-multiple-commands)
    - [Commands in Sequence](#commands-in-sequence)
    - [Special Characters of the Shell](#special-characters-of-the-shell)
  - [Control Structures](#control-structures)
    - [If and Else](#if-and-else)
  - [Sub Processes](#sub-processes)
  - [Looping](#looping)
  - [Globbing](#globbing)
  - [Phases of the Shell](#phases-of-the-shell)

## General Commands

### Basic Output Manipulation

---

Some basic commands and their most common arguments you should integrate into your workflow (and ones that will be used without warning from here on out). These are typically used as something to pipe output into to improve your experience:

- `wc [-cmlw]`: Output statistics about the number of bytes (-c), characters (-m), lines (-l), and/or words (-w) of the input stream or file(s).
- `head -n N`: Output only the first N lines of the input text.
- `tail -n N`: Output only the last N lines of the input text.
- `more`: Paging utility that lets you scroll through text a screenful at a time instead of having it be outputted all at once to the console. Like a read-only editor, it also supports interactive commands reminiscent of Vim keybindings and features like regex search.
- `less`: The direct upgrade to more, it also supports backwards navigation and more inclusive support for keybindings.

### Path & the Shell

---

If the name of a program does not contain any slashes, then the shell automatically looks through directories listed in the PATH environment variable to find the program name. This is why when you want to run an executable in the current directory, you have to use the ./executable syntax:

`PATH=$PATH:.` appends the current directory to path so you do not have to use the `./` notation

### Command Arguments

---

- Within shell languages, the simplest commands look like:

```bash
word0, word1, ..., wordn # word0 is the name of the program and word1, ...,
                         # wordn are the arguments to that program
```

- Normal (positional) arguments, like a.
- Options (aka **_flags_**) -ejh which is also equivalent to -e -j -h. Jamming them together is a thing you can do on Unix, but as we know from Assignment 2, this behavior becomes tricky when there are options that take arguments.
- Options that don't take any arguments are sometimes referred to as switches, and they set some kind of configuration simply by being present or absent (think of it like a boolean option, where presence means true and absence means false).

## Running Multiple Commands

### Commands in Sequence

---

- `;` is the sequencing operator which signifies a newline queing the following shell command after the character
- `&` is the parralellization operator which signifies that the command after that character will run in parallel
- `|` is the pipeline character which pipelines the output of one command as the input to another, and the pipe is a buffer
  - the pipe really depends on the read and write priviledges of the command
  - allows you to set up a sequence of little languages that each process or transform a single stream of text output as it makes its way into some final form.

### Special Characters of the Shell

```bash
  ~ # $ & * ( ) = [ ] \ | ; ' " < > ?

  $ echo 'hello\there\n"general kenobi"'
  hello here        # the \t is interpolated as an escape character
  "general kenobi"

  $ echo "hey there's\n\"general kenobi\""
  hey there's
  "general kenobi"
```

## Control Structures

### If and Else

---

```bash
cmd1 && cmd2    # run a command that executes properly, then run command 2
cmd1 || cmd2    # run command 2 if command 1 fails

if cmd1
  then cmd2
  else false
done

[ ] # takes arguments and does some of the obvious comparison functions and stuff

# Nested If Statements
if if [$a=$b]
		then cat file
		else grep x file
  then # If either then cat or grep x succeed, then go to the outer then

```

## Sub Processes

---

```bash
# Conditional Runtime Behavior
# Execute cmd1a, ignore exit, execute cmd1b and then execture cmd2 depending  on success or failure

{cmd1a; cmd1b;} && cmd2   # same process
(cmd1a; cmd1b;) && cmd2   # sub process
```

- the curly braces indicate the the shell is running the within the same process but changes the shells directory
- the paranthesis indicates that it changes to a different directory and does all work within a subprocess
  - safer but slower option

## Looping

---

```bash
for i in {1..100}
  do
    echo $i
done
```

## Globbing

---

- The shell will expand strings containing these special characters to every string that matches the pattern, separated by whitespaces
  - For example, `\*` in a directory containing files named `file1, file2, and file3` would expand to:
- This process is done by the shell and not the programs typically associated with the shell that provide the abstraction to the kernel/os

```bash
*           # any number of characters (does not match leading . as it messes with directory)
?           # any single character
[ ]         # matches a single character within a set, very similar to regEX but negation is ! not ^
{pdf,jpeg}  # - match multiple literals
[!]         # complement of a character set if ! is the first character
\           # escape character
```

`grep xyz *.c *-h-*`: &nbsp; matches all of the -h- expressions

## Phases of the Shell

1. Variable Expansion

```bash
${x+set} # expands to set if x has variable otherwise empty string
${x - nonempty} # expands to the string nonempty if x is nonempty
${x?} # expands to x otherwise throws and error
$ echo ${PATH?} # crash shell script if you dont have path
${x=default} # sets x to default if x is not set

# all of these work with : and ?


# set can be used to change the arguments to your command

set {args}
unset x
export x


$$ # is the shell
$! # is the pid of the last background process that your shell

kill $sleep
ps -ef | grep sleep
```

2. Tilde Expansion

```bash
# The Tilde will Turn into the Home Directory when $CALLS IT
x = ~
echo $x (tilde turns into /home/eggert)
```

3. Command Substitution

```bash
$(a b c d)

# shell stops, runs commands, then splices into the command we just ran
```

4. Arithmetic Expansion

```bash
$((x+5)) # will expand variables to do arithmetic (slow way to do it)
```

5. Field Splitting

```bash
x = 'a b c *c'
grep foo $x         # same argument
grep foo 'a b c *c' # same argument
grep foo a b c *c   # turns the space separated word into separate arguments
                    # a b c are separate arguments
```

6. Filename Expansion
7. Redirection
