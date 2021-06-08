import os
import json
from .runner import GhRunner

REPO_CONFIG_LOCATION = os.path.expanduser('~/.ghm/repos.json')


def fetch_buildpack_toml(repo):
    import urllib.request
    import subprocess

    fp = urllib.request.urlopen(
        f"https://raw.githubusercontent.com/{repo}/main/buildpack.toml")
    cmd = ["yj", "-tj"]
    res = subprocess.run(cmd, capture_output=True, check=True, input=fp.read())
    return json.loads(res.stdout)


def check_requirements():
    from subprocess import CalledProcessError
    try:
        GhRunner().help()
        return True
    except CalledProcessError:
        return False


def load_repos():
    """Loads a JSON formatted list of repositories to be used by the script"""
    repos = json.load(open(REPO_CONFIG_LOCATION))
    if not hasattr(repos, "append") or not hasattr(repos, "__len__"):
        raise TypeError("Invalid configuration file")
    return repos
