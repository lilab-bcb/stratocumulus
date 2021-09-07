import os, shutil
from subprocess import check_call

class LocalBackend:
    def __init__(self):
        self._backend = 'local'

    def copy(self, recursive, ionice, filenames):
        assert len(filenames) >= 2, "Either source or destination is missing!"
        target = filenames[-1]
        call_args1 = ['mkdir', '-p', target]
        print(' '.join(call_args1))
        check_call(call_args1)

        call_args = ['ionice', '-c', '2', '-n', '7'] if ionice and (shutil.which('ionice')) != None else []
        call_args += ['cp']
        if recursive:
            call_args.append('-r')
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)

    def sync(self, ionice, source, target):
        target = os.path.dirname(target)
        call_args = ['ionice', '-c', '2', '-n', '7'] if ionice and (shutil.which('ionice')) != None else []
        call_args += ['rsync', '-r', '--delete', source, target]
        print(' '.join(call_args))
        check_call(call_args)

    def delete(self, recursive, filenames):
        call_args = ['rm']
        if recursive:
            call_args.append('-r')
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)

    def stat(self, filename):
        call_args = ['stat', filename]
        check_call(call_args)
