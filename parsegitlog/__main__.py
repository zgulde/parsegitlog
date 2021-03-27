import argparse
import json
import sys

from parsegitlog.gitlog import get_commits

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="python -m parsegitlog")
    parser.add_argument("repo_path", default=".")
    parser.add_argument("-i", "--indent", type=int, default=2)
    args = parser.parse_args()

    output = get_commits(args.repo_path)
    indent = args.indent if args.indent > 0 else None
    print(json.dumps(output, indent=indent))
