# stdlib
import glob
import os
import subprocess

# package
from packagerbuddy import settings


def find_scripts(software: str, version: str) -> list[str]:
    scripts: list[str] = []

    version_agnostic = os.path.join(settings.DIR_SCRIPTS, software)
    if os.path.exists(version_agnostic):
        scripts.append(version_agnostic)

    results = glob.glob(f"{software}-{version}*", root_dir=settings.DIR_SCRIPTS)
    for result in results:
        path = os.path.join(settings.DIR_SCRIPTS, result)
        scripts.append(path)

    scripts.sort()
    return scripts


def run_script(script: str, software: str, version: str, wd: str | None = None) -> tuple[str, str]:
    args = [script, software, version]
    cmd = " ".join(args)
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        cwd=wd,
    )
    stdout, stderr = process.communicate()
    return stdout, stderr
