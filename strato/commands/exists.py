import argparse


example_text = """Examples:
  strato exists --backend aws s3://my-bucket/file1
  strato exists --backend gcp gs://my-bucket/folder2/
  strato exists --backend local folder2/
"""

def check_status(backend, filename, profile):
    assert backend in ['aws', 'gcp', 'local'], "Backend not supported!"

    if backend == 'aws':
        from strato.backends import AWSBackend
        be = AWSBackend()
        be.stat(filename, profile=profile)
    elif backend == 'gcp':
        from strato.backends import GCPBackend
        be = GCPBackend()
        be.stat(filename)
    else:
        from strato.backends import LocalBackend
        be = LocalBackend()
        be.stat(filename)

def main(argsv):
    parser = argparse.ArgumentParser(
        description="Check the existence of a file or folder, and raise an exception if not existing. \nNotice that a folder's path must end with '/'.",
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--backend', dest='backend', action='store', required=True, help='Specify which backend to use. Available options: aws, gcp, local.')
    parser.add_argument('--profile', dest='profile', type=str, action='store', help='AWS profile. Only works for aws backend, and use the default profile if not provided.')
    parser.add_argument('filename', metavar='filename', type=str, help='A file or folder path.')

    args = parser.parse_args(argsv)

    check_status(args.backend, args.filename, args.profile)
