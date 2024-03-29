# Version Control with Git

## Table of Contents

- [Version Control with Git](#version-control-with-git)
  - [Table of Contents](#table-of-contents)
  - [Control of Git](#control-of-git)
  - [Basic Git Commands](#basic-git-commands)
    - [Getting Started with Git](#getting-started-with-git)
    - [Basic Git Commands](#basic-git-commands-1)
    - [Git Log](#git-log)
      - [Exploring the Log](#exploring-the-log)
      - [Formatting the Log](#formatting-the-log)
  - [Making Changes](#making-changes)
  - [Commits: Options, Changing, and Syncing](#commits-options-changing-and-syncing)
    - [Writing Good Commit Messages](#writing-good-commit-messages)
    - [Changing Commits](#changing-commits)
    - [Syncing Commits](#syncing-commits)
    - [Viewing Differences](#viewing-differences)
  - [Configuring Git](#configuring-git)
    - [The .git/config File](#the-gitconfig-file)
    - [The ~/.gitconfig File](#the-gitconfig-file-1)
  - [Bisecting](#bisecting)
    - [Starting a bisect in Git](#starting-a-bisect-in-git)
    - [Edge Cases](#edge-cases)
  - [Tagging](#tagging)
    - [Annotated Tags](#annotated-tags)
    - [Implementation of Annotated Tags](#implementation-of-annotated-tags)
    - [Software Supply Chain Attacks](#software-supply-chain-attacks)
  - [Sub Modules](#sub-modules)
  - [Stashing](#stashing)
  - [Patching](#patching)

## Control of Git

Although there are many reasons for having version control systems, one important reason is that there are often multiple versions of histories that are present that often do not agree. In software development there are multiple versions of programs.

**There are Two things are under Git's control:**

1. Object database recording history of project development, where the project is modeled with a tree of files
   - basically everything that everyone did to the project
2. **Index**, or the cache records the future of the project or your plans for some of the future of the project
   - it keeps track of what you are going to do next, since you update the index and then commit it so that it turns into the past (migrating and emptying the index)
   - the motivation of this is so that you never commit anything that does not work yet

&nbsp;
&nbsp;
&nbsp;

## Basic Git Commands

### Getting Started with Git

---

- `git init` creates a repo from scratch
- `git clone URL` clones an existing repo
- `git init` followed by `git remote add NAME URL` will create a repo locally and then link it to a remote

**NOTE:** We don't necessarily have a "boss and servant" relationship between upstream and downstream repositories. Often times, a clone can become more active/popular than the original, in which case, the latter will start to sync with the former instead of vice versa.

### Basic Git Commands

---

- `git status` tells you updates to the index and the current state of the repo
- `git ls-files` lists std output names of all of the working files that is managed by git
- `git checkout` arranges for the working files to be what they were at a certain branch
- `git grep "pattern"` is basically the same as `grep pattern $(git ls-files)` searches the whole repo
- `git blame FILENAME` gives all of the authors of the commit, the time of the commit, and the shortened commit ID (unique prefix)

### Git Log

---

- `git log` gives the history of the changes made in the current repository to get it to the working order listed in the reverse time order
  - `SHIFT-G` takes us to the end of the repository
- allows us to inspect the object database (code) and the reason for the changes (message within the commit)
- The git log contains: COMMIT_ID (BRANCH), AUTHOR, DATE, COMMIT_MESSAGE
- the commit ID is the **checksum** of the commit contents
  - A checksum is like a fixed bit integer that is a function of the bytes of the content it is encoding (similar to a pointer to the content it is encoding)
  - This function must not produce **collisions**, where different contents produce the same checksum
    - 1/(2^160) is the chance of a collision due to the 160-bit number for the unique id
  - when you clone the database, you have the same ID's that represent the same commits (reason why it is a checksum)

#### Exploring the Log

---

- You can use the special `..` syntax to specify a commit range.

```shell
git log A..B # A Exclusive B Inclusive
```

```shell
git log B # Getting the _entire_ history _up to_ commit with ID B
```

You can also use **"version arithmetic"** to get references to commits based on aliases, like branch names, tag names, `HEAD`, etc.

> The special pointer `HEAD` by references the _current version_ of the repository. This is kind of like a "you are here" pointer. You can move it around such as checking out to other branches, a specific commit, etc. in which case `HEAD` moves to the corresponding commit and Git changes your project directory to match the snapshot of that commit.

- You can use the `^` syntax to specify the parent of a reference, so `HEAD^` means the commit just before `HEAD`, `HEAD^^` means the grandparent commit, etc.
- Example about showing the most recent commit:

```shell
git log HEAD^..HEAD
git log HEAD^!  # shorthand
```

#### Formatting the Log

---

```bash
git log --pretty=fuller
```

The fuller format shows that every commit has an **author** AND a **committer**, each with their own dates. Git distinguishes between these two contributors. This separation is routine for many larger projects. The author would be the person that writes the code, and the committer would be the overseer that reviews the and confirms the changes. These fields _establish responsibility_ for changes, a major reason for using version control in the first place.

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

## Commits: Options, Changing, and Syncing

- Commit messages are important because in essence, they help "market" your changes.
- tell readers of the repository why certain commits were made and whether it was a "good" commit by explaining the _motivation_ behind the changes
- The rationale behind commit messages are similar to why you should comment your code.
- There is overlap between comments in the source code and commit messages, but the primary distinction is the _audience_.
  - Commit messages are more historically oriented, what you would tell the "software historian," people interested in the development of the repository as a whole
  - Comments in the source code are for the "current developer," people interested in having to study or change your code

### Writing Good Commit Messages

- first line should be at most 50 characters, and this acts as the "subject line" for the commit, like the elevator pitch
  - gives any readers the _gist_ of the commit.
- The second line should be empty, separating the subject line from the body.
- The last line should be a larger description of the git command

### Changing Commits

---

- `git clean` removes all of the untracked files
- This is useful for removing files created as part of some build process. If you're not sure, you can run a "what if" with the `-n` option:
  > The `--dry-run`/`-n` switch is common to a lot of Git (and Unix in general) commands. It's a good way to "preview" the effects of a potentially destructive command instead of running it blindly right away.
- There's also the `-x` option which cleans files that will even be ignored:

### Syncing Commits

---

- The upstream repository is where you cloned the downstream repo from (probably the cloud)
  - the .git is the downstream repository
  - Consider you want to sync the downstream changes to some changes that were made to the upstream repo, you would use git fetch
- `git fetch` propagates the latest upstream repository within your downstream
  - git has two versions where one is "main" (current working directory), and one is "origin/main" (latest upstream); this differentiates your current changes from the changes that are upstream
  - git fetch changes the repositories idea of what upstream is within the repository and effectively does not change your current state (synced our opinion of upstream with what is actually upstream)
- `git pull` effectively fetching + copying it into your version of the repository - this is good when you have no changes on your side of the repository
  - if you make your own changes, there is a chance that you might collide with upstream, causing issues when using this method

Consider you clone and make a commit into your local repository.

```git
c1 <- c2 (master, origin/master)
c1 <- c2 (origin/master) <- c3 (master)
```

Now consider someone made a change and pushed to the remote and you pulled.

```
c1 <- c2 <- c4 (origin/master)
      ^- c3 (<- ^- )merge (master)
```

&nbsp;
&nbsp;
&nbsp;

### Viewing Differences

---

- `git diff` is similar to the GNU `diff` command, and like a more detailed version of `git status`

Viewing the difference between the _index_ and the _working files_: `Δ(index vs working files)`:

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

&nbsp;
&nbsp;
&nbsp;

## Configuring Git

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

After resolving the configuration in the current repository, Git then falls back to this configuration file. Contains _global_ configuration information for Git, like username and email.

<!-- From discussion notes. -->

You can edit this file manually with your editor of choice, but you can also use `git config` to write directly from the command line:

```shell
git config --global KEY VALUE
```

\*Setting up Git on New Machines:\*\*

```shell
git config --global user.name "Vincent Lin"
git config --global user.email vinlin24@outlook.com
```

The user name is not actually that important. It's mostly used for identifying contributors at a glance with things like `git log` I assume. The email however is _critical_ because remote services like GitHub use that to identify the account of the contributor.

## Bisecting

Suppose you have a linear piece of history where somewhere between a stable version and the most recent commit, something went wrong. You can think of this problem of finding the first faulty commit as partitioning the timeline into OK and NG ("not good") sections, hence _bisecting_.

The timeline is "sorted" in that if you think of OK=0 and NG=1, the history will always be such that all NGs follow OKs.

- This then becomes a classic _binary search_ problem, where we can identify the first NG commit in O(logN) time.

### Starting a bisect in Git

---

- `git bisect start HEAD v4.3`
  - Then we tell Git to run your check script on each commit and use the exit status to determine if the commit is OK or NG
- `git bisect run` where the run is your shell script will input any shell command that tests your command -> if it succeeds, it will continue, if it fails, it will stop and return that commit
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
```

&nbsp;
&nbsp;
&nbsp;

## Tagging

Suppose you want to get all of the source code of a specific version. You want a symbol that stands for a speciifc commit that never moves or changes in time.

- `git checkout v27`
- `git tag` lists all of the versions in alphabetical order
- `git tag REPO_NAME COMMIT_ID` creates a tag for the specific commit

Tagging is a big event within git. You would want the user to know about why the tag is being tagged in the first place. Thus, you can create something called annotated tag to get some metadata about that tag.

- you can have a branch and a tag named the same thing
- you can have many tags point to the same commit

### Annotated Tags

- `git tag -a theirversion -m "They liked the previous version" myvers^` creates an annotated tag with the name `theirversion` of the last commit of the repo `myvers`

### Implementation of Annotated Tags

- `ls -ltr $(find .git -type f) | less` we see a bunch of files that have been updated by the git tag command
  - when you look into the files, we can see the plain tags only have the commit id within the file
    - the normal tag is not a part of the git repository
  - the annotated tag is represented by an unique type of object within the git repository
    - the tag itself is an object but the tag also tags a commit object as well that has a lot of extra data with it

### Software Supply Chain Attacks

- people will write some code in a package that seems useful, but will actually exploit your system
  - people will use tags to ensure that the package is secure if the tag has someone trustworthy
  - to prevent faking identities, you would use a signed tag that has some sort of authentication (uses a cryptographic key)

&nbsp;
&nbsp;
&nbsp;

## Sub Modules

The reason a module would want to use a submodule is because we want to tie another package into our package and identify it with a commit id or specific version.

- Basically a pointer to another project containing a commit ID within the other project
- we can make changes to the latest version of another project, then you can pull the latest versions of the modules that you have copied
- `git submodule add https://github.com/a/b/c`
- This is similar to cloning, but instead of creating a new repository complete with its own `.git`, it:
  - Creates an empty subdirectory.
  - Create a `.gitmodules` file in the main project that establishes the relationship between the main project and the subdirectory
- Furthermore, updating a submodule is very simple. Instead of making edits to possibly to many files if you kept the dependency as part of your repository, the changes you make to the main project are simply which commit ID to use for the submodule
- This keeps both your code and cognitive load modularized.
- `git submodule foreach git pull origin master` for each submodule, pull each of the submodule differences

  &nbsp;
  &nbsp;
  &nbsp;

## Stashing

Consider you are working on a change but have to change your attention to something else.

- if you switch to a different branch with changes to the working directory, it will complain saying you have uncommitted work
  - if you commit, it will not be good and there will not be a clean commit
- `git stash push` saves the state of your working files in some part of the index. When you want to retrieve this state, you can get it from the stash stack with:

  - `git stash apply`

  &nbsp;
  &nbsp;
  &nbsp;

## Patching

- share repo over the network (bad/inefficient practice)
- email patches | only tells you the change to the code but not the metadata (author, details)
- `git format-patch` outputs the diff and the metadata of the changes in the commit
- `git am FILES...` imports commits from the email patches in the .mbox format
- The reason why we want to do this is because we want to ensure that people actually read the messages unlike when pull requests are made
