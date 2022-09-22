import argparse

from strato.commands.util import get_backend


example_text = """Examples:
  strato rm s3://my-bucket/file1 s3://my-bucket/folder2/
  strato rm -m gs://my-bucket/file1 gs://my-bucket/folder2 gs://my-bucket/folder3/*.zip
  strato rm file1 folder2
"""


def delete_files(recursive, parallel, filenames, profile, quiet, dryrun):
    backend = get_backend(filenames)

    if backend == "aws":
        from strato.backends import AWSBackend

        be = AWSBackend()
        be.delete(filenames, profile, quiet, dryrun)
    elif backend == "gcp":
        from strato.backends import GCPBackend

        be = GCPBackend()
        be.delete(recursive, parallel, filenames, quiet, dryrun)
    else:
        from strato.backends import LocalBackend

        be = LocalBackend()
        be.delete(recursive, filenames, quiet, dryrun)


def main(argsv):
    parser = argparse.ArgumentParser(
        description="Delete files or folders. \nNotice that for AWS backend, a folder link must end with a slash '/', and wildcards are not yet supported.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--profile",
        dest="profile",
        type=str,
        action="store",
        help="AWS profile. Only works for aws backend, and use the default profile if not provided.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        help="Recursive deletion. Not needed for AWS backend.",
    )
    parser.add_argument(
        "-m",
        dest="parallel",
        action="store_true",
        help="Run operations in parallel. Only available for GCP backend.",
    )
    parser.add_argument(
        "--quiet", dest="quiet", action="store_true", help="Hide the underlying command."
    )
    parser.add_argument(
        "--dryrun",
        action="store_true",
        help="Displays the operations that would be performed using the specified command without actually running them.",
    )
    parser.add_argument(
        "files", metavar="filenames", type=str, nargs="+", help="List of file paths."
    )

    args = parser.parse_args(argsv)
    delete_files(args.recursive, args.parallel, args.files, args.profile, args.quiet, args.dryrun)
