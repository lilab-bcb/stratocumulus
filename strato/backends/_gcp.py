from subprocess import check_call


class GCPBackend:
    def __init__(self):
        self._backend = 'gcp'

    def copy(self, recursive, parallel, filenames):
        call_args = ['gsutil', '-q', '-o', 'GSUtil:parallel_composite_upload_threshold=150M']
        if parallel:
            call_args.append('-m')
        call_args.append('cp')
        if recursive:
            call_args.append('-r')
        call_args.extend(filenames)
        print(' '.join(call_args))
        check_call(call_args)
