from parsegitlog.gitlog import parse_commit, parse_shortstat

shortstat_cases = [
    (
        " 1 files changed, 2 insertions(+)",
        dict(files_changed=1, insertions=2, deletions=0),
    ),
    (
        " 1 file changed, 2 deletions(-)",
        dict(files_changed=1, deletions=2, insertions=0),
    ),
    (
        " 1 file changed, 2 insertions(+), 3 deletions(-)",
        dict(files_changed=1, insertions=2, deletions=3),
    ),
    (
        "14 files changed, 20 insertions(+), 20 deletions(-)",
        dict(files_changed=14, insertions=20, deletions=20),
    ),
    (
        " 1 file changed, 3 deletions(-)",
        dict(files_changed=1, deletions=3, insertions=0),
    ),
    (
        " 2 files changed, 3 insertions(+), 18 deletions(-)",
        dict(files_changed=2, insertions=3, deletions=18),
    ),
    (
        " 1 file changed, 0 insertions(+), 0 deletions(-)",
        dict(files_changed=1, insertions=0, deletions=0),
    ),
]


def test_shortstat_parsing():
    for text, expected in shortstat_cases:
        assert parse_shortstat(text) == expected


TEST_COMMIT = """
b237cc62263073bb1060b59e370c6a5a3b8af6e8
2021-03-21T00:07:20-05:00
Zach Gulde
zachgulde@gmail.com
2021-03-21T00:07:20-05:00
Zach Gulde
zachgulde@gmail.com
a9a3ad8c5ef251b9b4559ea6abd6fc8571e037e4
Add command for port forwarding


 2 files changed, 31 insertions(+)
"""

TEST_LONGER_COMMIT = """
61bd079c5d9f82fa4efc5caf4a4dc47bf314816b
2021-02-28T21:11:51-06:00
Zach Gulde
zachgulde@gmail.com
2021-02-28T21:11:51-06:00
Zach Gulde
zachgulde@gmail.com
a59ab87075e477de4967ed640fdd6857bb654266
Rename config file to cods-config
Apparently spring boot will look for a `config` _directory_ in the
directory in which it is starting up to load configuration files from.

Cods also utilizes a `config` _file_ at /srv/example.com/config to
figure out how to copy sensitive files on the server.

This hasn't been an issue when last tested with springboot 2.1.x, but as
of 2.4.x the application fails to startup with a message about "config"
not being a directory.

Based on very brief testing it seems like this is only an issue when the
spring security dependency is added (!?). Rather that run it down or
reqeuire users to configure their spring boot apps differently, we'll
rename the cods configuration file.


 4 files changed, 12 insertions(+), 12 deletions(-)
"""


def test_commit_parsing():
    assert parse_commit(TEST_COMMIT) == {
        "author_email": "zachgulde@gmail.com",
        "author_name": "Zach Gulde",
        "authored_at": "2021-03-21T00:07:20-05:00",
        "body": "",
        "committed_at": "2021-03-21T00:07:20-05:00",
        "committer_email": "zachgulde@gmail.com",
        "committer_name": "Zach Gulde",
        "deletions": 0,
        "is_merge": False,
        "files_changed": 2,
        "insertions": 31,
        "parents": "a9a3ad8c5ef251b9b4559ea6abd6fc8571e037e4",
        "sha": "b237cc62263073bb1060b59e370c6a5a3b8af6e8",
        "subject": "Add command for port forwarding",
    }
    assert parse_commit(TEST_LONGER_COMMIT) == {
        "author_email": "zachgulde@gmail.com",
        "author_name": "Zach Gulde",
        "body": "Apparently spring boot will look for a `config` _directory_ in the\n"
        "directory in which it is starting up to load configuration files "
        "from.\n"
        "\n"
        "Cods also utilizes a `config` _file_ at /srv/example.com/config to\n"
        "figure out how to copy sensitive files on the server.\n"
        "\n"
        "This hasn't been an issue when last tested with springboot 2.1.x, "
        "but as\n"
        "of 2.4.x the application fails to startup with a message about "
        '"config"\n'
        "not being a directory.\n"
        "\n"
        "Based on very brief testing it seems like this is only an issue when "
        "the\n"
        "spring security dependency is added (!?). Rather that run it down "
        "or\n"
        "reqeuire users to configure their spring boot apps differently, "
        "we'll\n"
        "rename the cods configuration file.\n",
        "authored_at": "2021-02-28T21:11:51-06:00",
        "committed_at": "2021-02-28T21:11:51-06:00",
        "committer_email": "zachgulde@gmail.com",
        "committer_name": "Zach Gulde",
        "deletions": 12,
        "files_changed": 4,
        "insertions": 12,
        "is_merge": False,
        "parents": "a59ab87075e477de4967ed640fdd6857bb654266",
        "sha": "61bd079c5d9f82fa4efc5caf4a4dc47bf314816b",
        "subject": "Rename config file to cods-config",
    }
