from subprocess import check_call

class LocalBackend:
    def __init__(self):
        self._backend = 'local'

    def copy(self, recursive, filenames):
        assert len(filenames) >= 2, "Either source or destination is missing!"
        target = filenames[-1]
        call_args1 = ['mkdir', '-p', target]
        print(' '.join(call_args1))
        check_call(call_args1)

        call_args = ['cp']
        if recursive:
            call_args.append('-r')
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)
