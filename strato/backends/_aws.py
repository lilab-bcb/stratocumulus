from subprocess import check_call


class AWSBackend:
    def __init__(self):
        self._backend = 'aws'

    def copy(self, recursive, filenames):
        call_args = ['aws', 's3', 'cp', '--only-show-errors']
        if recursive:
            call_args.append('--recursive')
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)
