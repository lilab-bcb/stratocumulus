import argparse


def delete_files(backend, recursive, parallel, filenames):
    assert backend in ['aws', 'gcp', 'local'], "Backend not supported!"

    if backend == 'aws':
        from strato.backends import AWSBackend
        be = AWSBackend()
        be.delete(filenames)
    elif backend == 'gcp':
        from strato.backends import GCPBackend
        be = GCPBackend()
        be.delete(recursive, parallel, filenames)
    else:
        from strato.backends import LocalBackend
        be = LocalBackend()
        be.delete(recursive, filenames)

def main(argsv):
    parser = argparse.ArgumentParser(description="Delete files or folders. Notice that for AWS backend, a folder link must end with a slash '/'.")
    parser.add_argument('--backend', dest='backend', action='store', required=True, help='Specify which backend to use. Available options: aws, gcp, local.')
    parser.add_argument('-r', dest='recursive', action='store_true', help="Recursive deletion. Not needed for AWS backend.")
    parser.add_argument('-m', dest='parallel', action='store_true', help="Run operations in parallel. Only available for GCP backend.")
    parser.add_argument('files', metavar='filenames', type=str, nargs='+', help='List of file paths.')

    args = parser.parse_args(argsv)
    delete_files(args.backend, args.recursive, args.parallel, args.files)
