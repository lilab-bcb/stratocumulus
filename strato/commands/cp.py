import argparse

example_text = """Examples:
  # AWS upload
  strato cp --backend aws file1 folder2 s3://my-bucket/target_folder/
  # AWS download
  strato cp --backend aws s3://my-bucket/source_folder/*.zip /target_folder/

  # GCP upload
  strato cp --backend gcp -m -r --ionice file1 folder2 gs://my-bucket/target_folder/
  # GCP download
  mkdir /target_folder
  strato cp --backend gcp -m gs://my-bucket/source_folder/*.zip /target_folder/

  # On local machine
  strato cp --backend local -r file1 folder2 /target_folder/
"""

def copy_files(backend, recursive, parallel, ionice, filenames, profile, quiet):
    assert backend in ['aws', 'gcp', 'local'], "Backend not supported!"

    if backend == 'aws':
        from strato.backends import AWSBackend
        be = AWSBackend()
        be.copy(ionice, filenames, profile, quiet)
    elif backend == 'gcp':
        from strato.backends import GCPBackend
        be = GCPBackend()
        be.copy(recursive, parallel, ionice, filenames, quiet)
    else:
        from strato.backends import LocalBackend
        be = LocalBackend()
        be.copy(recursive, ionice, filenames, quiet)


def main(argsv):
    parser = argparse.ArgumentParser(
        description="Copy files or folders. \nNotice that for AWS backend, a folder link must end with a slash '/'. \nFor GCP backend, if the target is a non-existing local path, you need to manually create it beforehand.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--backend', dest='backend', action='store', required=True, help='Specify which backend to use. Available options: aws, gcp, local.')
    parser.add_argument('-r', dest='recursive', action='store_true', help="Recursive copy. Not needed for AWS backend.")
    parser.add_argument('-m', dest='parallel', action='store_true', help="Run operations in parallel. Only available for GCP backend.")
    parser.add_argument('--ionice', dest='ionice', action='store_true', help="Run with ionice to avoid monopolizing local disk's I/O. Only available for Linux.")
    parser.add_argument('--profile', dest='profile', type=str, action='store', help='AWS profile. Only works for aws backend, and use the default profile if not provided.')
    parser.add_argument('--quiet', dest='quiet', action='store_true', help="Hide the underlying cloud command.")
    parser.add_argument('files', metavar='filenames', type=str, nargs='+', help='List of file paths.')

    args = parser.parse_args(argsv)
    copy_files(args.backend, args.recursive, args.parallel, args.ionice, args.files, args.profile, args.quiet)
