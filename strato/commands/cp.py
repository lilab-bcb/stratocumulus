import argparse


def copy_files(backend, recursive, parallel, ionice, filenames):
    assert backend in ['aws', 'gcp', 'local'], "Backend not supported!"

    if backend == 'aws':
        from strato.backends import AWSBackend
        be = AWSBackend()
        be.copy(ionice, filenames)
    elif backend == 'gcp':
        from strato.backends import GCPBackend
        be = GCPBackend()
        be.copy(recursive, parallel, ionice, filenames)
    else:
        from strato.backends import LocalBackend
        be = LocalBackend()
        be.copy(recursive, ionice, filenames)


def main(argsv):
    parser = argparse.ArgumentParser(description="Copy files or folders. Notice that for AWS backend, a folder link must end with a slash '/'.")
    parser.add_argument('--backend', dest='backend', action='store', required=True, help='Specify which backend to use. Available options: aws, gcp, local.')
    parser.add_argument('-r', dest='recursive', action='store_true', help="Recursive copy. Not needed for AWS backend.")
    parser.add_argument('-m', dest='parallel', action='store_true', help="Run operations in parallel. Only available for GCP backend.")
    parser.add_argument('--ionice', dest='ionice', action='store_true', help="Run with ionice to avoid monopolizing local disk's I/O. Only available for Linux.")
    parser.add_argument('files', metavar='filenames', type=str, nargs='+', help='List of file paths.')

    args = parser.parse_args(argsv)
    copy_files(args.backend, args.recursive, args.parallel, args.ionice, args.files)
