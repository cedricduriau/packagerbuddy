def split_ext(path: str) -> tuple[str, str]:
    ext: str = ""
    supported_extensions = [".tar.gz", ".tar.bz", ".tar", ".zip"]
    for supported_extension in supported_extensions:
        if path.endswith(supported_extension):
            ext = supported_extension
            break

    root = path.replace(ext, "")
    return root, ext
