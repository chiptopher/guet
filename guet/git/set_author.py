import subprocess


def configure_git_author(name: str, email: str) -> None:
    process = subprocess.Popen(['git', 'config', 'user.name', name])
    process.wait()
    process = subprocess.Popen(['git', 'config', 'user.email', email])
    process.wait()
