# C Programming

## History of C++ and C

- the difference of C++ and C is the object oriented design portion of C
  - Things that are missing include (polymorphism, encapsulation, and inheritance)
- Structs having static data members and functions. Structs in C are strictly collections of data members (plain old data).
- Namespace control. C has a single top-level namespace.
- Overloading. There is a feature called `_Generic` that attempts a way around this, but this is esoteric.
- Exception handling. C has a system with `<setjump.h>` but it has all sort of trouble.
- Memory allocation built in. There is no `new` operator in C. Instead, you use the *library functions* `malloc()` and `free()`; they aren't built into the language itself.
- No `cin`/`cout`. You use IO with the library functions under the `<stdio.h>` header.

## Compilation

1. Preprocessing: `gcc -E foo.c >file.i` takes the macros expands them, and throws away the defintions
2. Conversion to Assembly: `gcc -S foo.c` turns the c code into the assembly representation that the CPU can understand
3. Conversion to Object Code: `gcc -c foo.s` turns the code into an object file, containing machine instructions with some loose holes that allow for all of the things that are in other modules
4. Link the object files together `gcc foo.o`: *fills in the blanks* within the file
5. Run Program -> copy the bytes into the RAM that will be executed

- You can link all of the steps at once with: `gcc main.c def.c -o main`
