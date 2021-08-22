from subprocess import check_call


class AWSBackend:
    def __init__(self):
        self._backend = 'aws'
        self._call_prefix = ['aws', 's3']

    def copy(self, recursive, filenames):
        call_args = self._call_prefix.copy()
        call_args.extend(['cp', '--only-show-errors'])
        if recursive:
            call_args.append('--recursive')

        source_files = filenames[:-1]
        target = filenames[-1]
        if len(source_files) > 1 and target[-1] != '/':
            target += '/'

        # Copy files one by one.
        for source in source_files:
            subcall_args = call_args.copy()
            subcall_args.extend([source, target])
            print(' '.join(subcall_args))
            check_call(subcall_args)

    def sync(self, source, target):
        call_args = self._call_prefix.copy()
        call_args.extend(['sync', '--delete', source, target])
        print(' '.join(call_args))
        check_call(call_args)

    def delete(self, recursive, filenames):
        call_args = self._call_prefix.copy()
        call_args.extend(['rm', '--quiet'])
        if recursive:
            call_args.append('--recursive')

        # Delete files one by one.
        for f in filenames:
            subcall_args = call_args.copy()
            subcall_args.append(f)
            print(' '.join(subcall_args))
            check_call(subcall_args)

    def stat(self, filename):
        call_args = self._call_prefix.copy()
        call_args.extend(['ls', filename])
        check_call(call_args)
