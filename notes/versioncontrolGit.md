# Version Control with Git

## Table of Contents

- [Version Control with Git](#version-control-with-git)
  - [Table of Contents](#table-of-contents)
  - [Version Control and History](#version-control-and-history)
  - [Control of Git](#control-of-git)
  - [Getting Started](#getting-started)
    - [Basic Information](#basic-information)
    - [Basic Git Commands](#basic-git-commands)
  - [Exploring the Log](#exploring-the-log)
    - [Narrowing the Log](#narrowing-the-log)
    - [Formatting the Log](#formatting-the-log)
  - [Commit Messages](#commit-messages)
  - [Making Changes](#making-changes)
  - [Commits and Staging](#commits-and-staging)
    - [Commit Options](#commit-options)
    - [Changing Commits](#changing-commits)
    - [Syncing Commits](#syncing-commits)
  - [Viewing Status of a Repository](#viewing-status-of-a-repository)
  - [Viewing Differences](#viewing-differences)
  - [Configuring Git](#configuring-git)
    - [The .gitignore File](#the-gitignore-file)
    - [The .git/config File](#the-gitconfig-file)
    - [The ~/.gitconfig File](#the-gitconfig-file-1)
  - [Show a Commit](#show-a-commit)
  - [Bisecting](#bisecting)
    - [Starting a bisect in Git](#starting-a-bisect-in-git)
    - [Edge Cases](#edge-cases)

## Version Control and History

- there are often multiple versions of history that people want to tell, they usually do not agree
  - in software development, we do not have the same problem but our stems from having multiple versions of programs
- With version control, you are making and creating the history as we go on
  - no one knew what was being running and version control gave us control over the software development processes

## Control of Git

- This is usually from the perspective of a software developer/manager, and in some cases, the end user trying to use the software.

**Two things are under Git's control:**

1. Object database recording history of project development, where the project is modeled with a tree of files
    - everything that everyone did to the project
2. **Index**, or the cache records the future of the project or your plans for some of the future of the project
   - it keeps track of what you are going to do next, since you update the index and then commit it so that it turns into the past (migrating and emptying the index)
   - the motivation of this is so that you never commit anything that does not work yet

## Getting Started

1. Starting a Git Repo from Scratch

    ```bash
    git init
    ```

2. Create one remotely on a server (like GitHub) and clone it

    ```bash
    git clone URL # you get a fresh copy of the source code, and all of the history of the project
    ```

3. Create one locally and then link it to a remote):

    ```shell
    git init
    git remote add NAME URL
    ```

### Basic Information

---

- **Cloning** copies a repository AND creates corresponding working files.
  - it remembers where you are cloning from

- Git sets up a special `.git` subdirectory, which is what makes the project directory a "repository".
  - this contains the object database and the index (history, all files, etc)

**NOTE:** We don't necessarily have a "boss and servant" relationship between upstream and downstream repositories. Often times, a clone can become more active/popular than the original, in which case, the latter will start to sync with the former instead of vice versa.

### Basic Git Commands

---

- `git status` tells you updates to the index and the current state of the repo
- `git ls-files` lists std output names of all of the working files that is managed by git
- `git checkout -F` arranges for the working files to be what they were at a certain commit
- `git grep "pattern"` = `grep pattern $(git ls-files)`
- `git blame` gives the author of the commit, the time of the commit, and the shortened commit ID (unique prefix)

&nbsp;
&nbsp;
&nbsp;

## Exploring the Log

- `git log` gives the history of the changes made in the current repository to get it to the working order
  - listed in the reverse time order
  - `SHIFT-G` takes us to the end of the repository
- allows us to inspect the object database (code) and the reason for the changes (message within the commit)
- We note that each commit has a unique ID, a long string after the word "commit", which is the **checksum** of the commit contents
  - A checksum is like a fixed bit integer that is a function of the bytes of the content it is encoding (similar to a pointer to the content it is encoding)
  - This function must not produce **collisions**, where different contents produce the same checksum
    - 1/(2^160) is the chance of a collision due to the 160-bit number for the unique id
  - when you clone the database, you have the same ID's that represent the same commits

### Narrowing the Log

---

- You can use the special `..` syntax to specify a commit range.
- The following displays the history between commits with ref `A` (exclusive) and `B` (inclusive), so like `(A, B]`.
  - This is like "show me everything that led up to B, but exclude everything that led up to A":

```shell
git log A..B
```

- Getting the *entire* history *up to* commit with ID `B`:

```shell
git log B
```

You can also use **"version arithmetic"** to get references to commits based on aliases, like branch names, tag names, `HEAD`, etc. [More on commit notation in Git Internals](Git%20Internals.md). The official documentation is also nice: <https://git-scm.com/docs/gitrevisions>.

> The special pointer `HEAD` by references the *current version* of the repository. This is kind of like a "you are here" pointer. You can move it around such as checking out to other branches, a specific commit, etc. in which case `HEAD` moves to the corresponding commit and Git changes your project directory to match the snapshot of that commit.

- You can use the `^` syntax to specify the parent of a reference, so `HEAD^` means the commit just before `HEAD`, `HEAD^^` means the grandparent commit, etc.
- Example about showing the most recent commit:

```shell
git log HEAD^..HEAD
git log HEAD^!  # shorthand
```

### Formatting the Log

---

```bash
git log --pretty=fuller
```

The fuller format shows that every commit has an **author** AND a **committer**, each with their own dates. Git distinguishes between these two contributors. This separation is routine for many larger projects. The author would be the person that writes the code, and the committer would be the overseer that reviews the and confirms the changes. These fields *establish responsibility* for changes, a major reason for using version control in the first place.

An interesting thing you may observe about repositories that have been developed for a long time is that you may notice commits with timestamps dating back to before Git was even around. This is because projects may have migrated from other version control systems, like RVS and CVS, and in copying over the history, the date data are all preserved.

<!-- From discussion notes. -->

Other examples:

```shell
git log --stat
git log --oneline
git log --pretty=format:"%h - %an, %ar: %s"
git log --oneline --decorate --graph --all

# Look for differences that change the occurrences of specified string
git log -S<string>
```

&nbsp;
&nbsp;
&nbsp;

## Commit Messages

- Commit messages are important because in essence, they help "market" your changes.
- tell readers of the repository why certain commits were made and whether it was a "good" commit by explaining the *motivation* behind the changes
  - "Why are you making this change? Why shouldn't I just revert it?"
- The rationale behind commit messages are similar to why you should comment your code.

- There is overlap between comments in the source code and commit messages, but the primary distinction is the *audience*.
  - Commit messages are more historically oriented, what you would tell the "software historian," people interested in the development of the repository as a whole
  - Comments in the source code are for the "current developer," people interested in having to study or change your code

Example commit message from the MIT repository shown in lecture:

```
Fix issues found by ASAN and Coverity

* tests/test_driver.pl: Preserve the LSAN_OPTIONS variable.
* tests/scripts/targets/ONESHELL: Don't set a local variable.
* tests/scripts/functions/let: Test empty let variable.
```

- first line should be at most 50 characters, and this acts as the "subject line" for the commit, like the elevator pitch
  - gives any readers the *gist* of the commit.
- The second line should be empty, separating the subject line from the body.
- The last line should be a larger description of the git command

&nbsp;
&nbsp;
&nbsp;

## Making Changes

1. Edit the working files.
2. Run `git add FILES...` to add the specified file contents to the index (the **staging area**, the **cache**)
   - if you edit the file that you have already added, there will be three versions of the file (file in the HEAD), (file in staging area), (file in the working directory)
     - when you commit, it is the recent version that you added, while the unstaged changes remain in the index (cache)
3. Run one of the `git diff` commands to verify that the changes are what you want.
4. Run `git commit`, which takes your index, makes a new commit, and puts it into the object database with the auto-generated checksum. In effect, it changes the commit `HEAD` references.

&nbsp;
&nbsp;
&nbsp;

## Commits and Staging

- **Commits** are like checkpoints for your code, snapshots that are saved in the repository. Commits *append the index to the history*.
- There is an intermediate phase between modified/unmodified files and commit called the **staging area**. You can add files to this phase with `git add`
- **Unstaging** a file `git restore ---staged FILE`
- `git ammend commit` will ammend the commit
  - this is not recommended in nonlocal repositories because when you are working with others, they might have commits getting pulled from underneath them causing issues with their code

### Commit Options

---

- You're probably familiar with `git commit -m MESSAGE` that every Git crash course teaches you
  - the default `git commit` actually drops you into your configured editor and allows you to write longer commit messages with the subject line and body format detailed above
- There is also `git commit -m MESSAGE FILE`, where `FILE` contains the extended message
  - This is useful for automating messages in scripting. Example:

```shell
git commit -m 'Fix issues from previous patch' README.git
```

### Changing Commits

---

- `git clean` removes all of the untracked files
- This is useful for removing files created as part of some build process. If you're not sure, you can run a "what if" with the `-n` option:

> The `--dry-run`/`-n` switch is common to a lot of Git (and Unix in general) commands. It's a good way to "preview" the effects of a potentially destructive command instead of running it blindly right away.

- There's also the `-x` option which cleans files that will even be ignored:

```shell
git clean -nx  # you best see what that would do first lol
git clean -x
```

### Syncing Commits

---

- The upstream repository is where you cloned the downstream repo from
  - the .git is the downstream repository
  - Consider you want to sync the downstream changes to some changes that was made to the upstream repo, you would use git fetch
- `git fetch` propogates the latest upstream repository within your downstream
  - git has two versions where one is "main" (current working on) and one is "origin/main" (latest upstream)
  - git fetch changes the repositories idea of what upstream is within the repository and effectively does not change your current state
- `git pull` effectively fetching + copy it into your version of the repository
  - if you make your own changes, there is a chance that you might collide with upstream causing issues when using this method

&nbsp;
&nbsp;
&nbsp;

## Viewing Status of a Repository

- Checking the status of your repository:

```shell
git status
```

Each file can be in the following states:

- Staged
- Not staged but modified
- Untracked

In general, files go through these states:

![Git Diagram](https://camo.githubusercontent.com/2f5084d2a28564283a8dff925fdf8fcf1e33377c1e879c33f94d2316f324654c/68747470733a2f2f6769742d73636d2e636f6d2f626f6f6b2f656e2f76322f696d616765732f6c6966656379636c652e706e67)

## Viewing Differences

`git diff` is similar to the GNU `diff` command, and like a more detailed version of `git status`.

> **HISTORICALLY:** The algorithm is very complex and was developed by a professor at the University of Arizona who went on to work on the Human Genome Project.

Viewing the difference between the *index* and the *working files*: `Δ(index vs working files)`:

```shell
git diff
```

This views the difference between the latest commit and the index: `Δ(latest commit vs index)`:

```shell
git diff --cached
git diff --staged  # equivalent
```

And this is `Δ(last commit vs working files)`

```shell
git diff HEAD
```

Compare the grandparent commit to the latest commit:

```shell
git diff HEAD^^..HEAD
```

<!-- From discussion notes. -->

More examples of viewing the difference between two commits:

```shell
# Typically with SHAs of the specific commits you want
git diff REF..REF

# But you can also abbreviate the hashes:
git diff 5c6cb30..53bf6bd
git diff 5c6c..54bf

# But this has a limit. This fails:
git diff 5c6..53b

# As usual you can use the HEAD ref to reference commits relative to
# the last commit:
git diff HEAD~..HEAD
git diff HEAD~4..HEAD
git diff HEAD^..HEAD
```

## Configuring Git

### The .gitignore File

A special file inside the repository containing file patterns that Git should not track. The file pattern syntax is similar to the familiar **globbing pattern** as the shell.

.gitignore is like a configuration file that instructs how users run Git. It's under Git's control i.e. it'll show up in `git ls-files`.

**What files should be ignored?**

Files that we do not want to put under version control. Obvious candidates include:

- Temporary files, `\#*`
- Machine-dependent code, `*.o`
- Imported files (from other packages)
- Authentication information (passwords/keys/etc.)
- Hashes of passwords? If it's intended for authentication, this would be just as bad as raw passwords, so ignore them too. Hashes enable **rainbow attacks** on the passwords where attackers try to crack the checksum algorithm.

### The .git/config File

You can view the current configuration of the Git program with:

```shell
git config -l
```

This outputs the information stored in the editable `.git/config` file, which is specific to the current repository. Cloning a repository also copies the configuration file.

**CAUTION:** One notable problem (which is standard across any software) is that if there is a syntax error in the configuration file, Git stops working altogether.

`.git/config` is NOT under version control because it determines how Git itself functions and because it would introduce the problem of recursion. `.gitignore` IS under version control because it's like a message from the developer and contains information about how to manage the project actually being version controlled. You also don't need to worry about what's in `.gitignore` to use Git itself.

### The ~/.gitconfig File

After resolving the configuration in the current repository, Git then falls back to this configuration file. Contains *global* configuration information for Git, like username and email.

<!-- From discussion notes. -->

You can edit this file manually with your editor of choice, but you can also use `git config` to write directly from the command line:

```shell
git config --global KEY VALUE
```

*Setting up Git on New Machines:**

```shell
git config --global user.name "Vincent Lin"
git config --global user.email vinlin24@outlook.com
```

The user name is not actually that important. It's mostly used for identifying contributors at a glance with things like `git log` I assume. The email however is *critical* because remote services like GitHub use that to identify the account of the contributor.

<!-- Added because I thought it was cool. -->

Other cool things you can specify in this file:

```ini
[core]
    # If you don't like being dropped into Vim by default,
    # This sets it to VS Code (you can also use Emacs, etc.)
    editor = code

[alias]
    # Abbreviations
    s = status
    co = checkout
    cm = commit -m
    # etc.
    # I have much more ehe
```

## Show a Commit

`git show` is a generic command that shows a commit "object". Commit objects live in the database and are really just the recorded changes from the previous commit along with some metadata.

The ubiquitous `--pretty` option can be used here too for more verbose output:

```shell
git show --pretty=fuller
```

## Bisecting

Suppose you have a linear piece of history where somewhere between a stable version and the most recent commit, something went wrong. You can think of this problem of finding the first faulty commit as partitioning the timeline into OK and NG ("not good") sections, hence *bisecting*.

The timeline is "sorted" in that if you think of OK=0 and NG=1, the history will always be such that all NGs follow OKs.

![Bisect](https://www.sumologic.com/wp-content/uploads/git-bisect-fig1.png)

- This then becomes a classic *binary search* problem, where we can identify the first NG commit in O(logN) time.

### Starting a bisect in Git

---

- `git bisect start HEAD v4.3`
  - Then we tell Git to run your check script on each commit and use the exit status to determine if the commit is OK or NG
- `git bisect run` input any shell command that tests your comamnd -> if it succeeds, it will continue, if it fails, it will stop and return that commit
- `git bisect run make check` this command will basically keep running the bisect with your test cases and will then return the command once you are done
  - the make check will recompile everything and then do the test, since the source code changes
  - the make files might change and git will run whatever the changed makefile will be

### Edge Cases

---

- `git bisect run timeout 100 make check` - will timeout after 100 seconds to ensure that you do not get caught in an infinate loop
- `git bisect run -j make check` changes the bisection procedure to run in parallel
- An edge case to consider is that a bug is fixed and then reintroduced, this might cause a lot of issues with the bisect

Of course, this also introduces the problem that if your test cases are buggy, then you may get false alarms. If you know ahead of time that a commit, say `v3`, will produce unreliable test results, you can skip it with:

```shell
git bisect skip v3
