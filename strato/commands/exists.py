import argparse


def check_status(backend, filename):
    assert backend in ['aws', 'gcp', 'local'], "Backend not supported!"

    if backend == 'aws':
        from strato.backends import AWSBackend
        be = AWSBackend()
        be.stat(filename)
    elif backend == 'gcp':
        from strato.backends import GCPBackend
        be = GCPBackend()
        be.stat(filename)
    else:
        from strato.backends import LocalBackend
        be = LocalBackend()
        be.stat(filename)

def main(argsv):
    parser = argparse.ArgumentParser(description="Check if a file or folder's path exists. Break if doesn't exist.")
    parser.add_argument('--backend', dest='backend', action='store', required=True, help='Specify which backend to use. Available options: aws, gcp, local.')
    parser.add_argument('filename', metavar='filename', type=str, help='A file or folder path.')

    args = parser.parse_args(argsv)

    check_status(args.backend, args.filename)
