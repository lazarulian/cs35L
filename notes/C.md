# C Programming

## History of C++ and C

C is the predecessor to C++, so it is missing a lot of ’features’ that C++ has. Some of these are:

- STL
- Classes and Objects
  - Polymorphism (foo(int& a) and foo(bool a))
  - Inheritance (class Dog: public Animal)
  - Encapsulation (private)
- Namespace Control
- Explicit use of static to create singular instances
- Exception Handling
- Memory Management: new and delete (wrappers for malloc() and free() respectively) (g) cin, cout, << >>
- Function Overloading

## Compilation

**1. Preprocessing (.c) -> (.i)**

- preprocessor replaces macro definitions in the source code with their corresponding values.
- preprocessor includes header files in the source code using the "#include" directive
- preprocessor evaluates conditional compilation directives such as "#ifdef",
- preprocessor removes comments from the source code

```C
gcc -E input.c -o output.i
```

**2. Conversion to Assembly (.c/.i -> .s)**

- turns the c code into the assembly representation that the CPU can understand

```C
gcc -S foo.c -o foo.s
gcc -S foo.i -o foo.s
```

**3. Conversion to Object Code (.s/.c -> .o)**

- turns the code into an object file, containing machine instructions with some loose holes that allow for all of the things that are in other modules

```C
gcc -c foo.s -o foo.o
gcc -c mylibrary.c -o mylibrary.o
```

**4. Linking (.o -> .out)**

- _fills in the blanks_ within the file (creates .so files)
- ".so" files are shared object files that are created by the compiler during the process of linking a program with shared libraries
  - Shared object files are libraries that are linked to a program at runtime rather than compile time
  - contain executable code and data that can be loaded into memory and used by multiple programs simultaneously
  - smaller than static libraries, and they can be loaded and unloaded dynamically

```C
gcc --shared -o libmylibrary.so mylibrary1.o mylibrary2.o
gcc output.o -o output
```

To load a shared library:

```C
// Load the shared library at runtime
void* handle = dlopen("./libexample.so", RTLD_LAZY);

if (!handle) {
    fprintf(stderr, "Error: %s\n", dlerror());
    return 1;
}
```

**5. Run Program**

- Run Program -> copy the bytes into the RAM that will be executed
- You can link all of the steps at once with: `gcc main.c def.c -o main`

```C
./foo
```

&nbsp;
&nbsp;
&nbsp;

## Linking

- **Static linking:** Static linking involves linking all necessary object files and libraries into a single executable file at compile time. This results in a self-contained executable file that can be run on any system with the appropriate operating system and processor architecture. However, this method can lead to larger file sizes and longer build times.
  - good for debugging since you have all of the files available
- **Dynamic linking:** Dynamic linking involves linking object files and libraries at runtime, allowing multiple programs to share a single copy of a library. This can lead to smaller file sizes and faster build times, as well as improved memory usage. However, it requires the presence of the necessary library files at runtime and can be more complex to manage.
- **Dynamic loading:** Dynamic loading involves loading object files and libraries at runtime, allowing a program to selectively load and unload libraries as needed. This can improve performance and reduce memory usage, as well as enable plugins and other dynamic behavior. However, it can be more complex to implement and requires careful management of memory and resources.
- **Incremental linking:** Incremental linking involves linking only the parts of an executable file that have changed since the last build, rather than re-linking the entire file. This can reduce build times and improve developer productivity, particularly for large projects with many source files and libraries.

&nbsp;
&nbsp;
&nbsp;

## System Calls

### read()

---

In C programming, the read() function is used to read data from a file or a file-like object. It takes the following parameters:

```C
ssize_t read(int fd, void *buf, size_t count);
```

- `fd`: the file descriptor of the file to be read
- `buf`: the buffer where the read data will be stored
- `count`: the maximum number of bytes to be read

The read() function reads up to count bytes of data from the file referred to by the file descriptor fd, and stores the data in the buffer buf. The function returns the number of bytes that were actually read, which may be less than count if the end of the file is reached or if an error occurs.

### open()

---

In C programming, the open() function is used to open a file and obtain a file descriptor, which is an integer that uniquely identifies the opened file in the operating system. The open() function takes the following parameters:

```C
int open(const char *pathname, int flags, mode_t mode);
```

- `pathname`: a string containing the name of the file to be opened
- `flags`: a bitwise OR of one or more of the following constants, which specify how the file should be opened:
- `mode`: a bitwise OR of one or more of the following constants, which specify the permissions to be set for the file if it is created by the O_CREAT flag:

The `open()` function returns a file descriptor on success, which is a non-negative integer, or -1 on failure, indicating an error.

### printf()

- %s - Take the next argument and print it as a string
- %d,i - Take the next argument and print it as an int
- %f,F - double in normal (fixed-point) notation
- %e,E - double value in standard form
- %g,G - double in either normal or exponential notation
- %x,X - unsigned int
- %o,O - unsigned int in octal
- %c - char (character)
- %p - void\* (pointer to void)
- %a - double in hexadecimal notation
- %n - Print nothing, but writes the number of characters written so far into an integer pointer parameter.

## Example

```C
#include <stdio.h>

char *c[] = {"the", "quick brown fox", "jumped", "over the", "lazy dog"};
char **cp[] = {c + 3, c + 2, c + 1, c, c + 4};
char ***cpp = cp;

int main(void)
{
    printf("%s\n", **(cpp + 3));    // prints (the)
    printf("%s\n", **(cp + 4) + 4); // prints ( dog) // plus four means go 4
    printf("%s\n", **(++cpp));      // prints (jumped) (second item c+3)
    printf("%s\n", **cp);           // prints (over the) (first item c+3)
    printf("%s\n", **(++cpp) + 5);  // prints (brown fox)
    return 0;
}
```
