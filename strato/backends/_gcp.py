from subprocess import check_call


class GCPBackend:
    def __init__(self):
        self._backend = 'gcp'
        self._call_prefix = ['gsutil', '-q', '-o', 'GSUtil:parallel_composite_upload_threshold=150M']

    def copy(self, recursive, parallel, filenames):
        call_args = self._call_prefix.copy()
        if parallel:
            call_args.append('-m')
        call_args.append('cp')
        if recursive:
            call_args.append('-r')
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)

    def sync(self, parallel, source, target):
        call_args = self._call_prefix.copy()
        if parallel:
            call_args.append('-m')
        call_args.extend(['rsync', '-d', '-r', source, target])
        print(' '.join(call_args))
        check_call(call_args)

    def delete(self, recursive, parallel, filenames):
        call_args = self._call_prefix.copy()
        if parallel:
            call_args.append('-m')
        call_args.append('rm')
        if recursive:
            call_args.append('-r')
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)

    def stat(self, filename):
        call_args = ['gsutil', '-q', 'stat', filename]
        check_call(call_args)
