# Debugging

## Methods to Debug

## Operational Tools

- Print statements
- `time` is a shell command that tells the amount of CPU time it takes to run a program
  - works on the unmodified program
- `ps` (process status) shows which processes take up the most time
- `ps -ef` print out all of the processes and their run time
- `ps -ejtf` print out all of the processes and their run time within a tree structure
- `top` list up the top 20 processes and how much time it has been taking
- `strace` a meta command that logs to standard error every system call that your program makes
  - these involve instructions to the kernel, instructions to hardware, c-library, graphics-library, etc.
- Valgrind is more intrusive than STRACE and looks at all of the instructions that it executes
  - finds bad memory access
  - access fixed storage

## System Calls

- A way for programs to interact with the operating system (api to the kernel)
- The concept of an **operating system** was invented to facilitate interaction between programs and the hardware.
  - Without it, it would be much easier for programs to maliciously attack hardware or cause I/O conflicts with read/write operations.
- Programs can make **system calls** *to* the operating system, and the operating system will then interact with the hardware in a well-defined way and report back with any output

### Categories of System Calls

1. Process control `fork`
2. File management `open`/`close` a file, `read`/`write`
3. Device management
4. information maintenance
5. Communication
6. Protection

### Stack Protection & Security

- `gcc -fstack-protection` allows you to call stack overflow bugs
  - This has to do with how the instruction pointer changes to a bogus part of program using buffer overflow attacks
  - the return instruction is the error
  - the fstack inserts extra code at the start of the program such that the location of the return address is not necessarily guarenteed and there is a stack canary
    - if the canary is dead, that means the buffer overflow attack has occured and the stack will be killed
    - This works because the attacker would have to overwrite the `randomvalue` to get to the bottom of the call frame to reach the return address, which is typically what they need to overwrite to continue their attack.
  - There is debate whether `-fstack-protector` is a default option. Some Linux distros like Debian and Ubuntu have it on by default. This is off by default on SEASnet. There's also the opposite option called `-fno-stack-protector` that turns the setting off.

## Performance Bugs & Optimization Flags

- The `-O`, `-O2`, `-O3`, etc. flags to specify the level of *optimization **for CPU usage***.
- `gcc -o` allows to slow down the compiler and then to improve the speed of the executable because of the optimizations it finds within the program
  - caches the registers
  - out of order execution
  - harder to debug because the code is a lot harder to read
- `gcc -o0` will allow for better debugging since the compile time is a lot faster
- `gcc -flto` performs link time optimizations that allow the o file to have a copy of the source code
  - way slower to compile and harder to debug
  - allows for source code level optimizations with the use case

### Performance Bug Improvements

- In GCC, there's a built-in function called `__builtin_unreachable()`
  - Your code should never call this function
  - The purpose of this is to mark a certain condition in your code as something that will never happen, so the compiler can optimize it away.
