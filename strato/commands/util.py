from subprocess import check_call
from urllib.parse import urlparse


def get_path_scheme(path):
    scheme = urlparse(path).scheme
    if len(scheme) <= 1:  # for file paths: /foo/bar/test.h5ad or C:/foo/bar/test.h5ad
        scheme = "file"
    return scheme


def makedirs(path, quiet, dryrun):
    call_args = ["mkdir", "-p", path]
    if not quiet or dryrun:
        print(" ".join(call_args))
    if not dryrun:
        check_call(call_args)


def get_backend(paths):
    backends = set()
    for path in paths:
        scheme = get_path_scheme(path)
        if scheme == "s3":
            backend = "aws"
        elif scheme == "gs":
            backend = "gcp"
        elif scheme == "file":
            backend = "local"
        else:
            raise ValueError("Unknown scheme {}".format(scheme))
        backends.add(backend)
    if len(backends) == 1:
        return backends.pop()
    # cloud backend gets a higher priority than local backend
    if "local" in backends:
        backends.remove("local")
    if len(backends) > 1:
        raise ValueError("Cross backend support not available")
    return backends.pop()
