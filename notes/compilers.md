# Compiler Internals

1. Preproccessing .c -> .i
2. Code Generation
3. Assembly
4. Machine Code
5. Run

## The Difficulty of Code Generation

- There are many coding languages and many different assembly languages as well
  - We have to write L x M compilers.
- GCC & Clang has common parts of the compiler and have n front ends and m backends
  - front-ends take the preprocessed output (software)
  - back-ends take the assembly code and turns into machine code
