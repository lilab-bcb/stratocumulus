import argparse

from strato.commands.util import get_backend


example_text = """Examples:
  # AWS upload
  strato cp file1 folder2 s3://my-bucket/target_folder/
  # AWS download
  strato cp s3://my-bucket/source_folder/*.zip /target_folder/

  # GCP upload
  strato cp -m -r --ionice file1 folder2 gs://my-bucket/target_folder/
  # GCP download
  mkdir /target_folder
  strato cp -m gs://my-bucket/source_folder/*.zip /target_folder/

  # On local machine
  strato cp -r file1 folder2 /target_folder/
"""


def copy_files(recursive, parallel, ionice, filenames, profile, quiet, dryrun):
    backend = get_backend(filenames)

    if backend == "aws":
        from strato.backends import AWSBackend

        be = AWSBackend()
        be.copy(ionice, filenames, profile, quiet, dryrun)
    elif backend == "gcp":
        from strato.backends import GCPBackend

        be = GCPBackend()
        be.copy(recursive, parallel, ionice, filenames, quiet, dryrun)
    else:
        from strato.backends import LocalBackend

        be = LocalBackend()
        be.copy(recursive, ionice, filenames, quiet, dryrun)


def main(argsv):
    parser = argparse.ArgumentParser(
        description="Copy files or folders.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-r",
        "--recursive",
        dest="recursive",
        action="store_true",
        help="Recursive copy",
    )
    parser.add_argument(
        "-m",
        dest="parallel",
        action="store_true",
        help="Run operations in parallel. Only available for GCP backend.",
    )
    parser.add_argument(
        "--ionice",
        dest="ionice",
        action="store_true",
        help="Run with ionice to avoid monopolizing local disk's I/O. Only available for Linux.",
    )
    parser.add_argument(
        "--profile",
        dest="profile",
        type=str,
        action="store",
        help="AWS profile. Only works for aws backend, and use the default profile if not provided.",
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
    copy_files(
        args.recursive,
        args.parallel,
        args.ionice,
        args.files,
        args.profile,
        args.quiet,
        args.dryrun,
    )
