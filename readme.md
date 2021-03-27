# parsegitlog

```
python -m pip install parsegitlog
```

## Context

I've been working on a project where I need to get information on every commit
from serveral hundred repos, and using
[GitPython](https://gitpython.readthedocs.io/en/stable/intro.html). GitPython is
great, but it was a little slow for what I was trying to do.

The method of parsing the gitlog in this project is much faster for my use case.

Note that this project is much more narrow in scope than GitPython, and relies
on parsing the output of `git log` directly, so might be more fragile.

You might find this useful if you only need to analyze the commits for a repo,
and not perform any other git operations progromatically.

## Usage

You can either import this as a module or run it from the command line.

### Command Line

```
python -m parsegitlog --help
```

```
python -m parsegitlog
```

### Importing

```python
from parsegitlog import get_commits

repo_path = '/path/to/my/git/repository'

get_commits(repo_path)
```

`get_commits` will return a list of dicts, each dict representing a single
commit from the repository.

## Gotchas

**_Merge commits will show up multiple times._** This is intended behavior.

Although they appear to be duplicates, the `files_changed`, `insertions`, and
`deletions` for each will be slightly different, and there will be duplicate
entries for each merge commit corresponding to the number of parents in the
merge. This is because, depending on which parent we compare to, the difference
from the parent (in terms of files changed, insertions, and deletions) won't be
the same (every other property should be the same).

