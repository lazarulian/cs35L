## How Debuggers Work

GDB is actually a separate process from the process being debugged. It uses special system calls to exert some control over the process being debugged. Model:

```
(gdb process)--+
               | special system calls
               v
        (your process)
```

These special system calls include, at any point in execution:

- Starting/stopping/continuing
- Accessing memory
- Accessing registers

These do have security restrictions and cannot be used arbitrarily. These restrictions depend on the OS, but typically the rule is that the debugger must control a process with _same user ID_. Other OS may have a more restrictive rule, stating it can only debug a _child process_.

## Getting Started with Debugging: GCC

You can use a `-g` flag to specify debug info level for a C program:

```shell
gcc -g3 program.c
```

This conflicts with optimization because code that is optimized by the compiler tends to become harder to understand.

```shell
gcc -g3 -O2 program.c
```

This typically results in [**inlining**](#inlining), where calls to functions can be optimized away by substituting their body into places where it was called. The produced machine code would then be functionally equivalent but have lost the information that a function was even called.

What the `-g` flag does is bloat the resulting object and executable files with debugging tables. This data isn't visible when the program runs normally, but debuggers will be able to access them.

> **ASIDE:** `_FORTIFY_SOURCE` is a standard technique used by GCC to make stack overflows less likely to succeed. For technical reasons, this is incompatible with no optimization i.e. attempting `gcc -O0` will cause a compiler error.

## Starting GDB

Dropping a program into GDB:

```shell
#   vvvv program to debug
gdb diff
```

Setting the working directory of the program when it starts up:

```console
(gdb) set cwd /etc
```

Setting environment variables for the debugging session:

```console
(gdb) set env TZ America/New_York
```

A defense technique against buffer overflow attacks is to have the program run at randomized locations in memory (CS 33). By default, Linux executes programs in an environment with randomized addresses for the stack, heap, C library, etc. and many even the `main()` function.

The downside of this program is that it will run differently every time. This means that if there's a bug that depends on stack addresses for example, then it may appear sometimes and not for others. This makes debugging harder, so by default, this option is already on:

```console
(gdb) set disable_randomization on
```

Actually running the program. The arguments you supply after `run` are in shell syntax and forwarded to the executable being debugged:

```console
(gdb) run -u /etc/os-release - < /dev/null
```

_Alternatively_, you can make GDB be in charge of another program using the PID of running process, effectively suspending it.

```console
(gdb) attach 986317
```

Releasing the program:

```console
(gdb) detach
```

### Controlling Your Program

`^C` stops the program. GDB takes control.

`*(int *)0=27` crashes the program and falls under GDB's control.

Continue running the code:

```console
(gdb) # c
(gdb) continue
```

Single step through the source code. Similarly, single step through the machine code.

```
(gdb) # s
(gdb) step
(gdb) # si
(gdb) stepi
```

Stepping can be tricky because there isn't always a sequential mapping of source code lines to machine code lines. Stepping through some machine code lines may make it look like the program is jumping back and forth between source code lines instead of running one-by-one in order.

A courser-grained variant of the `step` command. Advancing to the next line of source code at the current function call level i.e. a single step but without worrying about function calls, stepping "over" them. Similarly, it has a machine code version.

All these commands control the **instruction pointer**, e.g. `%rip` on x86-64.

```console
(gdb) # n
(gdb) next
(gdb) # ni
(gdb) nexti
```

Finish the current function and then stop:

```console
(gdb) fin
```

You can use **breakpoints** to stop the program at a certain instruction, typically a function name. Creating a breakpoint:

```console
(gdb) # b
(gdb) break analyze
(gdb) break diff.c:19
```

Listing your current breakpoints and their numbers:

```console
(gdb) info break
```

Deleting a breakpoint by number:

```console
(gdb) del 19
```

**How does GDB implement breakpoints?**

GDB takes the process being debugged and modifies its machine code. It stomps on the machine code of the specified function/line/instruction by zapping the first byte with a special instruction that is guaranteed to cause the program to trap, allowing GDB to take control.

**How does GDB implement watchpoints?**

Single step through the code, and after each instruction, see if `p` has changed. This can be really slow unless youh have special hardware support for watchpoints. Many CPUs, including x86-64, have this support.

### Other GDB Commands

---

**Printing a C expression (or register values):**

```gdb
(gdb) # p
(gdb) print expr
(gdb) print $rax
(gdb) print a[5]
(gdb) print cos(3.0)
```

It does more than just allow you to look at data. It lets you run a subroutine like `cos` in the program, which can modify the data and/or call arbitrary code from other parts of the program.

---

**Disassembling Code to Assembly**

```GDB
(gdb) disas cos
```

- disassembling a function to get the assembly code:

---

**Creating Checkpoints**

```
(gdb) checkpoint
```

- a snapshot of all of the variables and information about a state of the program
  - You can set a **checkpoint** and then run the code from the checkpoint by its number:

```
(gdb) restart 42
```

- starts command from wherever the checkpoint is

---

**Working with Other Architectures**

```gdb
(gdb) target
```

- For **cross-debugging**, you can specify what target you want to run in
  - basically you are debugging a program on a different architecture than the one that it is written in
  - the target will tell GDB the machine that the computer will be running on

---

**Going Back Instructions**

```
(gdb) rc
```

This command goes to the last instruction. GDB keeps track of all of the states in the program and it stores the step within memory (expensive operation)

- The inverse of `continue` is `reverse-continue` (`rc`)
  - This means to start running the program backwards until it hits the most recent breakpoint that it passed
- `(gdb) continue` goes forward in time

---

**Watching Variables**

```gdb
(gdb) watch p
```

- you can use **watchpoints** to tell the program to run until the specified variable `p` changes value
  - can be done with single stepping within the machine code but is expensive
    - there is often hardware support for watching four locations
  - useful to figure out what went wrong with the program dadsda

---

### Compiler Optimizations with GDB

There are certain things that might come up and cause issues when using GDB.

- Order of execution is different from what might be written
- the variables might be optimized away
  - we can look at the optimization flags but they are harder to debug
