import argparse

from strato.commands.util import get_backend


example_text = """Examples:
  strato sync source_folder s3://my-bucket/target_folder
  strato sync -m --ionice source_folder gs://my-bucket/target_folder
  strato sync source_folder target_folder
"""


def synchronize_folders(parallel, ionice, source, target, profile, quiet, dryrun):
    backend = get_backend([source, target])

    if backend == "aws":
        from strato.backends import AWSBackend

        be = AWSBackend()
        be.sync(ionice, source, target, profile, quiet, dryrun)
    elif backend == "gcp":
        from strato.backends import GCPBackend

        be = GCPBackend()
        be.sync(parallel, ionice, source, target, quiet, dryrun)
    else:
        from strato.backends import LocalBackend

        be = LocalBackend()
        be.sync(ionice, source, target, quiet, dryrun)


def main(argsv):
    parser = argparse.ArgumentParser(
        description="Synchronize source and target folders.\nNotice that this synchronization deletes extra files in the target folder not found in the source folder.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
    parser.add_argument("source", metavar="source", type=str, help="Source folder path.")
    parser.add_argument("target", metavar="target", type=str, help="Target folder path.")

    args = parser.parse_args(argsv)
    synchronize_folders(
        args.parallel, args.ionice, args.source, args.target, args.profile, args.quiet, args.dryrun
    )
