import subprocess
import os
from pathlib import Path


def run_as_root(script_path: Path):
    if not script_path.is_file():
        print(f"can't execute {script_path} not a file")
        return
    if not os.access(script_path, os.X_OK):
        print(f"can't execute {script_path} not executable")
        return

    path: str = str(script_path)
    subprocess.run([path])


def run_as_user(script_path: Path):
    if not script_path.is_file():
        print(f"can't execute {script_path} not a file")
        return
    if not os.access(script_path, os.X_OK):
        print(f"can't execute {script_path} not executable")
        return
    path: str = str(script_path)
    original_user = _get_original_user()
    cmd = ["runuser", "-P", "-u", original_user, path]
    subprocess.run(cmd)


def _get_original_user() -> str | None:
    """
    use SUDO_USER environment variable to get the name of the original user
    this should be set by the sudo command but if it isn't the logname command is used as a fallback
    """
    return os.environ.get("SUDO_USER") or _get_logname()


def _get_logname():
    """
    returns the users log in name
    instead of the current user so in my case it will
    always return ben instead of root or something similar
    returns none if the logname command failed
    """
    try:
        return subprocess.run(
            ["logname"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return None
