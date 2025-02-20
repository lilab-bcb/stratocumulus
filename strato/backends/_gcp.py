import shutil
from subprocess import DEVNULL, check_call


class GCPBackend:
    def __init__(self):
        if shutil.which("gcloud") is None:
            raise Exception("google-cloud-sdk is not installed!")
        self._backend = "gcp"
        self._call_prefix = [
            "gcloud",
            "storage",
            "--no-user-output-enabled",
        ]

    def copy(self, recursive, ionice, filenames, quiet, dryrun):
        # FIXME make local target directories to mimic behavior of aws and local backends
        call_args = (
            ["ionice", "-c", "2", "-n", "7"]
            if ionice and (shutil.which("ionice") is not None)
            else []
        )
        call_args += self._call_prefix
        call_args.append("cp")
        if recursive:
            call_args.append("-r")
        call_args.extend(filenames)
        if not quiet or dryrun:
            print(" ".join(call_args))
        if not dryrun:
            check_call(call_args)

    def sync(self, ionice, source, target, quiet, dryrun):
        # If target folder is local.
        if len(target.split("://")) == 1:
            import os

            if not os.path.exists(target):
                os.mkdir(target)

        call_args = (
            ["ionice", "-c", "2", "-n", "7"]
            if ionice and (shutil.which("ionice") is not None)
            else []
        )
        call_args += self._call_prefix
        call_args.extend(["rsync", "--delete-unmatched-destination-objects", "-r", source, target])
        if not quiet or dryrun:
            print(" ".join(call_args))
        if not dryrun:
            check_call(call_args)

    def delete(self, recursive, filenames, quiet, dryrun):
        call_args = self._call_prefix.copy()
        call_args.append("rm")
        if recursive:
            call_args.append("-r")
        call_args.extend(filenames)
        if not quiet or dryrun:
            print(" ".join(call_args))
        if not dryrun:
            check_call(call_args)

    def exists(self, filename):
        assert filename.startswith("gs://"), "Must be a GS URI!"
        call_args = ["gcloud", "storage", "ls", filename]
        check_call(call_args, stdout=DEVNULL)
