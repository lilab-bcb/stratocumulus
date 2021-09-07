import argparse


def synchronize_folders(backend, parallel, ionice, source, target):
    assert backend in ['aws', 'gcp', 'local'], "Backend not supported!"

    if backend == 'aws':
        from strato.backends import AWSBackend
        be = AWSBackend()
        be.sync(ionice, source, target)
    elif backend == 'gcp':
        from strato.backends import GCPBackend
        be = GCPBackend()
        be.sync(parallel, ionice, source, target)
    else:
        from strato.backends import LocalBackend
        be = LocalBackend()
        be.sync(ionice, source, target)

def main(argsv):
    parser = argparse.ArgumentParser(description="Synchronize source and target folders.")
    parser.add_argument('--backend', dest='backend', action='store', required=True, help='Specify which backend to use. Available options: aws, gcp, local.')
    parser.add_argument('-m', dest='parallel', action='store_true', help="Run operations in parallel. Only available for GCP backend.")
    parser.add_argument('--ionice', dest='ionice', action='store_true', help="Run with ionice to avoid monopolizing local disk's I/O. Only available for Linux.")
    parser.add_argument('source', metavar='source', type=str, help='Source folder path.')
    parser.add_argument('target', metavar='target', type=str, help='Target folder path.')

    args = parser.parse_args(argsv)
    synchronize_folders(args.backend, args.parallel, args.ionice, args.source, args.target)
