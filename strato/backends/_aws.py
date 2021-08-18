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
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)

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
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)

    def stat(self, filename):
        call_args = self._call_prefix.copy()
        call_args.extend(['ls', filename])
        check_call(call_args)
