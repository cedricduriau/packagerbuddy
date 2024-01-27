# stdlib
import subprocess


def run_script(script: str, software: str, version: str, wd: str | None = None) -> tuple[bytes, bytes]:
    args: list[str] = [script, software, version]
    cmd = " ".join(args)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=wd)
    stdout, stderr = process.communicate()
    return stdout, stderr
