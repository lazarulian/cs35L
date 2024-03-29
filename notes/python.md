# The Python Programming Language

## Table of Contents

- [The Python Programming Language](#the-python-programming-language)
  - [Table of Contents](#table-of-contents)
  - [History of Python](#history-of-python)
    - [Part 1: BASIC and ABC](#part-1-basic-and-abc)
    - [Part 2: Th Programming Language](#part-2-th-programming-language)
    - [Perl Python Combination](#perl-python-combination)
  - [Why Python?](#why-python)
  - [Python Internals](#python-internals)
    - [Typing](#typing)
  - [Lists](#lists)
    - [ASIDE: Underying `list` Allocation](#aside-underying-list-allocation)
  - [Python vs. Shell vs. Emacs Scripting](#python-vs-shell-vs-emacs-scripting)
  - [Classes and OOP](#classes-and-oop)
    - [Dunders and "Operator Overloading"](#dunders-and-operator-overloading)
    - [Namespaces in Classes](#namespaces-in-classes)
  - [Modules](#modules)
    - [The `import` Statement](#the-import-statement)
  - [Packages](#packages)
    - [The `PYTHONPATH` Environment Variable](#the-pythonpath-environment-variable)

&nbsp;
&nbsp;
&nbsp;

## History of Python

- From `grep` to `sed` to `awk`, such commands attempt to generalize and expand what the previous does, rising in levels of complexity.
- The **Perl** programming language was designed to be able do everything awk, etc. can do.
  - **Python** was designed to do everything Perl, etc. can do. The rise of Python can be attributed to two parts:

### Part 1: BASIC and ABC

---

- **BASIC**: an instructional language
- Instead of writing very low-level code, go up one level of abstraction. People were given a language that:

  - Hash tables are implemented into the language, like `set` and `dict`
  - All the basic algorithms already built-in. Just `sort` lol.
  - Enforce indentation.
  - An IDE to run the programs.

- High school students will then be programming in this new language called **ABC**. It didn't work because employers still wanted production ready languages.

### Part 2: Th Programming Language

---

> Perl = sh + awk + sed + ... (putting all the little languages together)

- Perl was designed as an antidote to the "Little Languages" philosophy, so it combined all the little languages into one scripting language.
  - Perl became the scripting language of choice for about 10 years.
  - It was designed to be like a real spoken language - there was always more than one way to do something.

### Perl Python Combination

---

**Python emerged as a combination of:**

- ABC had the philosophy that there is one correct way to do anything.
- The capabilities of Perl.
- Python is a scripting language that tries to do everything. Theoretically, if you know the language very well, you do not have to touch the little languages of the shell

> **ASIDE:** All 3 languages, BASIC, Perl, and Python can be either compiled or interpreted.

&nbsp;
&nbsp;
&nbsp;

## Why Python?

- **CONS:** Slow, memory hog.
- **PROS:** Easier to write (development cost vs. runtime cost). A lot of libraries are also written in C/C++ code for a performance bonus, made possible by **native method interfaces**.
- Scripting languages like Python demonstrate an alternate balance between development cost and runtime cost
  - Oftentimes, human time is much more valuable than computer time.
- Prevalent in machine learning
  - this feat is probably due to being at the right place at the right time. Python happened to be a reasonable scripting language for the job when the field was emerging in popularity.

> There's always going to be a time where you're the blind person next to the elephant. The goal of software construction is to make you a better blind person. **- Dr. Eggert**

&nbsp;
&nbsp;
&nbsp;

## Python Internals

- Python is **object-oriented**.
- It started with functions but no classes.
- When classes were introduced, they implemented _methods_ as functions that explicitly take the `self` first argument, which is actually how OOP is implemented behind the hood in languages like C++.

Anyway, every value is an object. Every object has:

- Identity - _cannot be changed_
- Type - _cannot be changed_
- Value - _can_ be changed, but only if the object is **mutable**

### Typing

- In old Python, `int` used to have a fixed size, so there was a distinction between integers and longs.
- The main _categories_ of types in modern Python:

**Singletons**: Types with only one instance throughout runtime

- `None`: Python's version of a `null` value
- `True` and `False`: Python's booleans, which (fun fact) actually subclass the numeric type `int`.

**Numbers**

- `int`: A number without a fractional part. In modern Python, these can be any size, so you don't need to worry about bounds/overflow like in most languages.
- `float`: A number with a fractional part. There's also the special `float("inf")` constant that represents infinity (`1/0` in C, `Infinity` in JavaScript, etc.).
- `complex`: A number with a real and imaginary part. You can initialize a literal with the `a+bj` syntax e.g. `5+4j`.

**Collections**

- **Sequential Containers**: Collections where order matters, with elements being accessed by **index**

  - `list`: Python's built-in vector type. Heterogenous, arbitrary-sized, ordered collections.
  - `tuple`: Same as `list`, but immutable, so it's fixed length. These are nice because they are more efficient and are in a sense "safer" to use.

- **Associative Containers**: Collections where elements are accessed by **key**

  - `set`: Python's built-in hash table. An unordered collection of unique, **hashable** values.
  - `dict`: Python's built-in hash map. Unordered collections of key-value pairs. Keys must be unique and **hashable**.

**Callables**: Objects that support being called with optional arguments

- **Functions**: objects you define with the `def` keyword or anonymous ones with the `lambda` keyword
  - functions are objects that can be called but can also be stored into another object and get called from that object (called callback)
    - `f = lambda x,y: x+y+1`
    - `g = f`, where g is now a callable `g(3, 19)`
      - `if g is f -> True`
- **Methods**: function objects bound to an instance of a class. They take a mandatory `self` positional argument, the class instance the method acts on behalf of.
- Callables can be **formatted with arguments**:
  - `def printf(fmt, *args)`: formats into tuple
  - `def printx(fmt, **args)`: formats into dictionary
    - `printx("abc def", a = 17, b = 19, c = -7)` results in `args = {'a' : 17, 'b':19}`

There's also the **buffer** type. I assume this is only available in Python 2. Buffers are like multiple strings. When you're done working with it, you can convert it to a string with `str(x)`.

## Lists

Common `list` methods:

- `my_list.append(value)`: add any value as an element to the end of the list.
- `my_list.extend(iterable)`: lay all the values out from the iterable as elements at the end of the list.
- `my_list.insert(index, value)`: insert an element at a position in the list, pushing everything after it backwards.
- `my_list.count(value)`: return the number of occurrences of `value` (using `==` checking).
- `my_list.remove(value)`: remove the first occurrence of `value` (using `==` checking), raising `ValueError` if not found.
- `my_list.pop([index])`: defaults to last item, which you can use along with `.append` to emulate a stack data structure. Raises `IndexError` if empty.
- `my_list.clear():` remove all elements.

Common operations universal to sequential containers:

- `len(my_list)`: return the number of elements.
- `my_list[i:j]`: return a `slice` of the container, starting from index `i` and up until but excluding `j`.
  - Mutable ones also support this syntax on the LHS, where it means **reassigning** a segment of the container, as well as `del my_list[i:j]`, which deletes that segment of the container.

### ASIDE: Underying `list` Allocation

- Probably uses cache size to determine starting size.
- After that, reallocation uses geometric resizing (approximately nine-eights according to [mCoding](https://www.youtube.com/watch?v=rdlQzhP71pQ)).
- The total cost of calling `list.append` N times is $O(N)$. Because the **amortized cost** of this operation is $O(1)$.

**Visualization:** imagine that the list length is doubled for every allocation, which isn't true, but this doesn't change the asymptotic time, so it simplifies the derivation:

```
[e e e e e e e e e e e e e e e e e e e e e e]
  ... |<3>|<--2 ops-->|<-------1 op-------->|
```

The total cost is O(1) overall.

&nbsp;
&nbsp;
&nbsp;

## Python vs. Shell vs. Emacs Scripting

- Lisp is an ASL for Emacs, like an extension language. It uses existing code, _Emacs primitives_.
- Shell uses existing programs.
- Python was designed to be a _general-purpose programming language_, so there are no "primitives" you bring together
  - you just write in the language altogether to program from scratch
    - it also converges to the same phenomenon where programmers glue together existing modules like PyTorch and SciPy
- What makes a language a scripting language supports this pattern of software construction of building applications from existing code

> The goal of a **scripting language** is you don't code from scratch. You glue together other people's code. You provide the cement, and the other people provide the bricks. **- Dr. Eggert**

## Classes and OOP

- Class hierarchies are **directed acyclic graphs (DAG)**.
- This is especially apparent because, unlike languages like Java, Python supports **multiple inheritances**.

- Python's **method resolution order (MRO)** is depth-first, left-to-right. So for example, if you define a class that inherits like so:

```python
class C(A, B):
    def some_method(self, arg):
        pass
```

- With the DAG model, this design makes it so that if `A` and `B` disagree, `A` will always take priority.

**Historical ASIDE:** The decision to explicitly include `self` in all method definitions was to not abstract a fundamental mechanism of OOP

- every method is _bound_ to the class and _acts on_ the instance
- If you examine the machine code of similar OOP languages like C++, you'll see that there's a hidden first argument to every method, which is the pointer to the object that the method is acting _on behalf of_

**Introspection ASIDE:** You can use the built-in `__mro__` attribute of class objects to programmatically access a class' method resolution order. For example:

```python
# Print the names of the classes in class O's MRO
print([cls.__name__ for cls in O.__mro__])
```

### Dunders and "Operator Overloading"

---

The old way to redefine the comparison operators:

```python
def __cmp__(self, other):
    # negative for <, 0 for equal, positive for >
    return num
```

- This is still supported but it is now anachronistic approach because you can run into hardware problems
- A notable example is the case of _floating point numbers_, which have an additional state, **NaN**, beyond negative, zero, and positive
  - we have the familiar `__lt__`, `__gt__`, etc.

This is the Python 2 predecessor to the familiar `__bool__` method:

```python
def __nonzero__(self):
    # Return whether the object is considered to be "not zero"
    return b
```

### Namespaces in Classes

---

- **Namespaces** are just dictionaries
- Classes have a special attribute `__dict__`, a `dict` that maps names to values
  - This gives rise to opportunities to write "clever" Python code, where you can programmatically alter the definition of an existing class:

```python
c = C()
c.__dict__["m"] is c.m
```

```python
class SimpleNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def __repr__(self):
        keys = sorted(self.__dict__)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(items))
```

- above is a cool example of changing some of the namespaces
- This is (probably) how **metaclasses** are implemented, which was not mentioned in lecture but is cool to know. They're basically classes that determine how other classes should be implemented.

&nbsp;
&nbsp;
&nbsp;

## Modules

### The `import` Statement

1. Creates a namespace for the module.
2. Executes the contents of the module _in the context of that namespace_. Eggert didn't mention this, but this step is actually only performed if the module _hasn't already been imported_. Modules are only run onces.
   - this is so that different classes with the same name do not collide with each other
3. Adds a name, the module name, to the current namespace.
   - all of the names are visible, but you have to type in modulename.(method)
   - `from modulename import *` never do this as this will wipe out other namespaces

Proof for #2:

```python
# module.py
print("Hello world")
```

```python
# runner.py
import module
import module
```

```console
$ python3 runner.py
Hello world
```

&nbsp;
&nbsp;
&nbsp;

## Packages

- Packages organize source code into a familiar tree structure
  - This allows importing to be parallel the file system.
- packages are about software developers (organized for convenience of developers)
- classes are organized for the behavior of your objects at runtime
- in python importing is a statement while in C++ it is a declaration
  - if tool > 1200: import trig (works in python)

The special `__init__.py` scripts turns a directory into a proper package, and it is automatically run upon import.

### The `PYTHONPATH` Environment Variable

---

Just as how [`PATH` instructs the shell program where to search for commands](Shell.md#path-and-resolving-command-names), `PYTHONPATH` instructs the Python interpreter on where to search for code.

Determines the behavior of the `import` statement. Python will search through the sequence of paths, delimited by colons (Unix) or semicolons (Windows), to search for names of packages or modules to import. The path to the standard library is included in `PYTHONPATH` by default.

Official documentation: <https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH>.

This variable is stored in and can be modified programmatically with `sys.path`, which is a `list[str]` containing the individual string paths.

**Why all this complexity with packages vs classes?**

Packages are oriented towards developers (like a _compile-time notion_). The tree is structured so that different developers can work on different parts of the code.

Classes are about runtime behavior (a _runtime notion_). You want inheritance to be independent of package hierarchy. Classes are only concerned with their own behavior, "what to do next", so it should be able to pull code from anywhere in the codebase. How developers _organize_ that codebase is made possible with packages.

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({ tex2jax: {inlineMath: [['$', '$']]}, messageStyle: "none" });
</script>
