# Build Tools

## Audience for Build Tools

- **Coders:** These people write the actual source code.
- **Builders:** These people are in charge of assembling the pieces of the program into a coherent application. They "run make".
- **Distributors:** These people take the built products and ship them out to the users. They "run Debian".
- **Installers:** These people take the output of the distributors and install them on the machines.
- **Testers:** These people try to find problems in the code or any of the steps after it like distribution and installation. These are often done by people lower in the chain, like interns.
- **Users:** These people are the intended consumers of the product.

### Creating a Simple Build Tool

You write your own project-specific build tools. Suppose you have a simple example of multiple C files that you need to link together. You could write a build script `build.sh`:

1. Maintainability
2. Expense of Recompilation of Entire Programs
3. Organization of the Build Script
4. Optional Features
5. Slow Compilation due to lack of Parallelization
6. Compiler Versioning - fixed by makefile

```shell
gcc -c x.c
gcc -c y.c
gcc -c z.c
gcc x.o y.o z.o -o foo
```

> Your goal as a software developer is to automate yourself out of a job. You constantly want to take the things that you're doing and automate it. **- Dr. Eggert, probably**

## Make and Makefiless

- A simple build tool intended to be a level up from a shell script is **Make**.
  - motivated from scripts taking too long to execute
  - they were inefficient because they would compile the entire program even if only one file was edited, so it does a lot of unnecessary work
- Thus, the essence of the **Makefile** is that you write a set of **recipes** in it, each of which instructing how to build a file
  - When you run `make`, the program does the *minimum amount of work* necessary to build the file
  - It does this with the concept of **prerequisites**.
- Make is a dynamic program that builds itself around the shell

## Anatomy of a Makefile

Make is like a hybrid language. The `target: prerequisites` lines are its own "Makefile" language. The recipes are in the shell language, commands that you would write at the terminal:

```makefile
CC = gcc
x.o: x.c
  $(CC) -c x.c
y.o: y.c
  $(CC) -c y.c
z.o: z.c
  $(CC) -c z.c
foo: x.o y.o z.o
  $(CC) $< -o $@
  # Escaping the $ so the shell can see it
  echo $$PATH
```

- makefile relies on the file timestamps and dependencies to see which files need to be rebuilt
- the makefile looks at the timestamp of the output and the timestamps of its prerequisites,  to determine what files have changed since last run (last modified time of each file).
  - If a file is up-to-date, it doesn't need to touch it.
  - the timestamp can be an issue if the server times are not in sync
- Often times, bugs arise from specifying the *dependencies* of the targets.
  - A *missing* dependency means the product may be wrong. Make will falsely assume its job is done if it does not know if needs to act on a certain file.
  - An *extraneous* dependency is a more benign mistake. Files are still compiled the same way as before, but it may cause Make to do extra work.
- `cc $(OBJ) -o $@`  automatically replaces the `$@` by the thing you are trying to build

### Macros

- Allows for people to shorten items that need to build or be called

```makefile
OBJ = a.o b.o c.o
foo: $OBJ
```

Commonly you'll see people define `CC` for the compiler command (`gcc`) and `CFLAGS` for the compiler options:

```makefile
CC = gcc
CFLAGS = -O2 -g3 -Wall -Wextra
```

```makefile
XYZ = foo1.o foo2.o foo3.o  # XYZ is a macro
foo: XYZ
  g++ XYZ -o foo
```

### Running the Make File

- If you do not tell the make file what to build first, it will build the first thing