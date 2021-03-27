import json
from parsegitlog.gitlog import get_commits
import sys

if __name__ == "__main__":

    output = get_commits(sys.argv[1])
    print(json.dumps(output, indent=2))
