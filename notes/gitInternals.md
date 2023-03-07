# Git Internals

- generally have to do with data-structures that persist (they stay there when the program finishes running)

## Plumbing vs. Porcelain

- the **porcelain** is the high-level commands for the end users
- the **plumbing** part of a program is the low-level part, where the actual work is done. It is not easy to use and not meant to be easy

Git actually violates a common software engineering rule, which is "Just show the porcelain to the outside world. Don't expose your plumbing.

Instead, Git wants to have two levels. Even at the low-level, it wants to expose its basic model for how Git works if the user is willing to understand how it works.

## .git Folder

The entire state of the repository is encoded in the special `.git` directory.

### Compatibility Issues

---

- When a new version of Git comes out, it needs to be able to work with old repositories (to maintain **backwards compatibility**)
- The converse is not always true; repositories created by recent versions of Git may not necessarily work with older versions of Git
  - therefore there are some files in the `.git` folder that are archaic.

### Anatomy of the Sub Directory

---

- `branches` - obsolescent - will appear when there are branches within the thing
- `config` - repository-specific configuration (very standard)
  - tends to act as the barrier to git providing important information about the repository
- `description` - used for GitWeb, an attempt to put Git on the web (somewhat obsolete)
- `HEAD` - where the current (default) branch is
- `hooks/*` - executable scripts that Git will invoke at certain "pressure points" (important triggers, like making a commit). By default, there are no working hooks; default ones all end with `.sample`, which illustrate what you might want to put in such hooks.
  - changing the config files will change the hooks most of the time
  - you can use these basically to set a certain behaviors within repositories
- `index` - a list of planned changes for the next commit in a binary data structure
  - the on file representation of what the future looks like
- `info/exclude` - addition to `.gitignore`.
  - .gitignore is a working file while this is private to a specific repository
- `logs` - keeps track of where the branches have been (histories of branch tip locations).
- `objects` - where the actual "repository" is, where the object database is stored.
  - object database contains pointers to the objects, and the objects point to each other
  - subdirectories are 2 hexadecimal digits and then 38 hexadecimal digits
    - you need to compute the checksum for the object
- `refs` - where the branch tips and tags are (where all the "pointers" in the repository are).
- `packed-refs` - optimized version of `refs`.

> **Emacs Hooks ASIDE:** Because `git clone` does NOT copy hooks, fresh local copies of a repository always have no functioning hooks. Emacs maintainers went around this by preparing a script in the Emacs source code called `autogen.sh`. This script creates a bunch of Git hooks that tailor the repository to be the way the Emacs developers want it to be tailored. This is a nice "gatekeeper" approach that ensures your development is relatively clean.

&nbsp;
&nbsp;
&nbsp;

## Comparison to File Systems

- It seems that Git uses a collection of files to represent a repository (and the index)
  - In reality, Git actually uses a combination of secondary storage and RAM (cache)
- A local Git repository and the index are made up of **objects** and some other auxiliary files
  - Git objects are like a tree of files in the filesystem.
- **REMINDER:** Every file has a unique index, namely the **inode number**, which you can see with `ls -i`.

Analogously, SHA-1 checksums for Git objects have the role that inode numbers have in filesystems. They are comparable to pointers in C/C++, values that uniquely identify the actual objects they reference.

**DIFFERENCE:** Files in the filesystem can be mutable. inode numbers thus exist _independently_ of the contents of their files. However, checksums uniquely identify objects _by their content_. Therefore, you **cannot** change objects' contents.

**SIMILARITY:** Both are directed acyclic graphs (DAGs). In the filesystem, it's guaranteed by the OS that you cannot have cycles. For Git objects, you cannot create a cycle because you can only _add_ to history, not change it.
