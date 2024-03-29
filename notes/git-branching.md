# Branching Merging and Rebasing

## Table of Contents

- [Branching Merging and Rebasing](#branching-merging-and-rebasing)
  - [Table of Contents](#table-of-contents)
  - [Branching in Git](#branching-in-git)
    - [Reasons for Branching](#reasons-for-branching)
    - [Details of Branching](#details-of-branching)
  - [Branching Commands](#branching-commands)
    - [Detached HEAD States](#detached-head-states)
  - [Patching Across Branches](#patching-across-branches)
  - [Merging in Git](#merging-in-git)
    - [Types of Merges](#types-of-merges)
    - [Mechanism of Merging](#mechanism-of-merging)
  - [Rebasing](#rebasing)
  - [Merging vs. Rebasing](#merging-vs-rebasing)

## Branching in Git

### Reasons for Branching

---

- A problem with doing a linear history, is it does not allow for parallelism
  - branches address this problem allow for people to change details of a larger codebase
  - a branch can be thought of as maintaining multiple alternate histories
- You might start a feature branch because it is not ready for everyone within the development team to use so you might create a branch to do work without impacting other people's work
- Upstream branches are useful because you get references to your remote repositories and you essentially know if you are ahead of them or not

### Details of Branching

---

- A branch is a lightweight movable pointer to a commit
  - the pointer can move to the start of the new commits as well
- One branch, the "main"/"master" branch is typically reserved for _mainline development_.
  - There may be other branches for things like _maintenance development_, _old releases_, _hot fixes_, etc.

```bash
git clone repo      # head point to the current commit
git branch z100     # head points to current commit at z100
git add foo.c
git commit          # head points to commit at foo.c in z100 branch
git add bar.c
git commit          # head points to commit at bar.c in z100 branch
git checkout main   # head points to the first commit in the main branch
git add bazz.c
git commit          # the main and head will point to first commit, origin/main will point to bazz.c
```

- in this example, origin/main is a read only copy of the upstream
  - you are meant to pull or fetch this and not edit this

&nbsp;
&nbsp;
&nbsp;

## Branching Commands

- `git branch -d branchname` deletes a branch (deletes the pointer to the branch)
- `git branch -D branchname` force deletes a branch (still a pointer to the branch)
- `git checkout -b newbranch commitid` will create a new branch from a commit ID
  - Branch names must be unique, git won't let you create or rename a branch to an existing name
  - this is because information about branches are stored as physical files in the file system under `.git`.
- `git branch -m a b` moves branch a to the name b (just renaming)

### Detached HEAD States

---

- `git checkout REF` You can checkout to an arbitrary commit by ID/tag name
  - this puts you in **detached HEAD state**, which is when `HEAD` is not pointing to any branch tip
  - Git warns you that you can look around but not make further changes
  - You cannot commit in this state because Git does not know how.
- However, if you want to make changes from this version of the codebase, you can checkout to a new branch off this commit as you normally would
  - `git checkout -b mybranch`

## Patching Across Branches

Suppose a security hole was discovered in an old commit, which multiple branches share as an ancestor. You can fix the bug on the mainline branch, but that doesn't solve it for other branches.

The solution is to **cherry-pick fixes**. You manually apply the same Δ to all versions that have the same bug.

Suppose there's an alternate branch named `maint`.

```shell
# Your familiar sequence
git add F
git commit -m "Make an emergency fix"

# Prepare the patch to apply to other branches
git diff HEAD^! > t.diff

# t.diff is a working file, preserved across checkout
git checkout maint

# Apply patch to this branch's working files
patch < t.diff
git add F
git commit -m "Make an emergency fix"
```

- The `patch` command is actually external to `diff`. It reads the output of the diff file and modifies the old file so that it looks like the new file:
- This modifies `A` to look like `B`
- this type of technology allows for the version control system to operate in small changes and compressing repositories
  - they only store the changes in the code lines rather than the actual entire file changes
- Attempting to apply a patch to a since edited version of a file may fail to work
- It may still work if the changes to the original files does not _collide_ with what the patch is attempting to change.
- `diff` operates on **hunks**, batches of lines that represent a change. Patching goes through each hunk and applies the change. If the hunks do not match, then it will reject the change into an `rej` file, prompting you to fix it by hand.
- `diff3 file1 file2 file3` compares three different files and checks for the differences of the three files
  - computes the difference between A&B and A&C and then it merges the two results
  - A is the common ancestor of B and C, you can _basically_ run diff on A&B and B&C and then runs it one last time to see the differences
  - git merge works the same way when there are colliding changes to the file
- **NOTE:** The output of `diff` is NOT deterministic. There is no requirement of the algorithm to modify a file in a specific way as long as the final copy is correct.

&nbsp;
&nbsp;
&nbsp;

## Merging in Git

- the tool that we use to add the changes within a branch into another branch
  - this commit will have more than one parent
- `diff A B >A-B.diff` will show us the difference between two files
- Merges cannot have any cycles and must be a directed acyclic graph
- When looking at a git log, you will see a linear representation that work since git will run a topological sort on your DAG

### Types of Merges

---

- Merging with conflicts
- Merging without conflicts
  - although there are no textual changes, there might be some semantic changes that make things very difficult
  - imagine you remove a function in a merge but there is some other merge that calls that function you removed

### Mechanism of Merging

---

Suppose:

```
                      this is the merge commit
                              v
()<--(A)<--()<--()<--(Y)<--(Merged)<-- ...
      |                       |
      +------()<----(X)<------+
```

- Git finds the common ancestor `A`, of the parent commits `X` and `Y`. Then, it runs computation on all 3. It is as if Git runs:

```shell
diff3 X A Y > combined.diff  # "3-way diff"
```

- This file describes changes to change the common ancestor `A` to _either_ `X` or `Y`.
  - Git then applies those changes and creates a _new_ commit instance for it, the **merge commit**.
- The command to merge a branch named `BRANCH_NAME` into the current branch: `git merge BRANCH_NAME`

What this does is:

1. Compute 3-way merges.
2. Replace working files accordingly.

## Rebasing

- Merging is often hard to have people review the work that you are doing since it is hard to look through the changes that you have made
- Alternatively, one can **rebase** a commit onto another branch
  - This takes away the problem where reviewers have to worry about common ancestry and a bunch of diffs. They only need to examine a linear history
  - Bisect works well with this but has a hard time working on the merge
- When rebasing, the branch off of the master, will show up after the current master when merging in the git log
- `git checkout b`
- `git rebase main`

```git
(c1)<--(c3) (main)
    |
    +--c2 (feature)
    Δ1
# After Rebase
c1<-c3(main)<-c2(feature)
```

## Merging vs. Rebasing

| Merging                                                                                                                | Rebasing                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ➕ Only one commit is created per merge.                                                                               | ➖ A new commit is made for every commit you rebase.                                                                                                                                                                                                             |
| ➕ Does not change existing commit history, so you're less likely to screw over others working on the same branch.     | ➖ Changes existing commit history. If you misuse this command, you could mess up an important branch like `main` for everyone else. See [the Golden Rule of Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing#the-golden-rule-of-rebasing). |
| ➕ Your steps can be fully retraced because you know when each merge was performed.                                    | ➖ It is difficult to see when a rebase actually occurred.                                                                                                                                                                                                       |
| ➖ If you have to merge often, these merge commits may pollute your history and make it harder to understand.          | ➕ No unnecessary merge commits polluting your history, making it easier to understand.                                                                                                                                                                          |
| ➖ Your history will still have interweaving branches that may make navigation (`git log`, `git bisect`, etc.) harder. | ➕ Keeps your history as linear as possible, making it easier to navigate with such commands.                                                                                                                                                                    |
