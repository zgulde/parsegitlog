"""
TODO: parse with --shortstat
"""
import json
import re
from subprocess import check_output


def parse_shortstat(content: str):
    content = content.strip()
    output = {}
    parts = content.split(", ")

    for part in parts:
        if "file changed" in part or "files changed" in part:
            output["files_changed"] = int(re.search(r"\d+", part).group())
        elif "insertion" in part:
            output["insertions"] = int(re.search(r"\d+", part).group())
        elif "deletion" in part:
            output["deletions"] = int(re.search(r"\d+", part).group())
        elif part == "":
            pass
        else:
            raise ValueError("Unknown shortstat part: %s" % part)
    if "insertions" not in output:
        output["insertions"] = 0
    if "deletions" not in output:
        output["deletions"] = 0
    return output


def parse_commit(commit: str):
    lines = commit.strip().split("\n")
    # some merges (maybe empty commits too? in practice i've only seen this with merges) don't do anything
    # and git won't print shortstat info for them. Handle this case here
    if len(lines) >= len(PRETTY_FORMATS) + 2:
        shortstat = parse_shortstat(lines[-1])
        body = "\n".join(lines[len(LABELS) - 1 : -2])
    else:
        shortstat = parse_shortstat("")
        body = "\n".join(lines[len(LABELS) - 1 :])
    d = dict(zip(LABELS[:-1], lines))
    d["body"] = body
    d["is_merge"] = "," in d["parents"]
    return {**shortstat, **d}


# something unique that won't show up in the log
SEPARATOR = "***********zgulde.gitlog.separator***********"

PRETTY_FORMATS = [
    ("sha", "%H"),
    ("authored_at", "%aI"),
    ("author_name", "%an"),
    ("author_email", "%ae"),
    ("committed_at", "%cI"),
    ("committer_name", "%cn"),
    ("committer_email", "%ce"),
    ("parents", "%P"),
    ("subject", "%s"),
    ("body", "%b"),
]

LABELS = [t[0] for t in PRETTY_FORMATS]
PLACEHOLDERS = [t[1] for t in PRETTY_FORMATS]
GITLOG_FORMAT = "%n".join([SEPARATOR] + [f[1] for f in PRETTY_FORMATS])


def get_commits(repo_path="."):
    cmd = ["git", "log", "-m", "--shortstat", f"--pretty={GITLOG_FORMAT}"]
    commits = check_output(cmd, cwd=repo_path).decode().split(SEPARATOR)
    # SEPARATOR comes at the start of each commit, so the first element here is empty
    commits = commits[1:]
    output = [parse_commit(commit) for commit in commits]
    return output


if __name__ == "__main__":
    import sys

    output = get_commits(sys.argv[1])
    print(json.dumps(output, indent=2))
