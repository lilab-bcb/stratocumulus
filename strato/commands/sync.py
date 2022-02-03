import argparse

example_text = """Examples:
  strato sync --backend aws source_folder s3://my-bucket/target_folder
  strato sync --backend gcp -m --ionice source_folder gs://my-bucket/target_folder
  strato sync --backend local source_folder target_folder
"""

def synchronize_folders(backend, parallel, ionice, source, target, profile, quiet):
    assert backend in ['aws', 'gcp', 'local'], "Backend not supported!"

    if backend == 'aws':
        from strato.backends import AWSBackend
        be = AWSBackend()
        be.sync(ionice, source, target, profile, quiet)
    elif backend == 'gcp':
        from strato.backends import GCPBackend
        be = GCPBackend()
        be.sync(parallel, ionice, source, target, quiet)
    else:
        from strato.backends import LocalBackend
        be = LocalBackend()
        be.sync(ionice, source, target, quiet)

def main(argsv):
    parser = argparse.ArgumentParser(
        description="Synchronize source and target folders.\nNotice that this synchronization deletes extra files in the target folder not found in the source folder.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--backend', dest='backend', action='store', required=True, help='Specify which backend to use. Available options: aws, gcp, local.')
    parser.add_argument('-m', dest='parallel', action='store_true', help="Run operations in parallel. Only available for GCP backend.")
    parser.add_argument('--ionice', dest='ionice', action='store_true', help="Run with ionice to avoid monopolizing local disk's I/O. Only available for Linux.")
    parser.add_argument('--profile', dest='profile', type=str, action='store', help='AWS profile. Only works for aws backend, and use the default profile if not provided.')
    parser.add_argument('--quiet', dest='quiet', action='store_true', help="Hide the underlying cloud command.")
    parser.add_argument('source', metavar='source', type=str, help='Source folder path.')
    parser.add_argument('target', metavar='target', type=str, help='Target folder path.')

    args = parser.parse_args(argsv)
    synchronize_folders(args.backend, args.parallel, args.ionice, args.source, args.target, args.profile, args.quiet)
