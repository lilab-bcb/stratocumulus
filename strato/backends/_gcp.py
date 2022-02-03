import shutil
from subprocess import check_call


class GCPBackend:
    def __init__(self):
        self._backend = 'gcp'
        self._call_prefix = ['gsutil', '-q', '-o', 'GSUtil:parallel_composite_upload_threshold=150M']

    def copy(self, recursive, parallel, ionice, filenames, quiet):
        call_args = ['ionice', '-c', '2', '-n', '7'] if ionice and (shutil.which('ionice') != None) else []
        call_args += self._call_prefix
        if parallel:
            call_args.append('-m')
        call_args.append('cp')
        if recursive:
            call_args.append('-r')
        call_args.extend(filenames)
        if not quiet:
            print(' '.join(call_args))
        check_call(call_args)

    def sync(self, parallel, ionice, source, target, quiet):
        # If target folder is local.
        if len(target.split('://')) == 1:
            import os
            if not os.path.exists(target):
                os.mkdir(target)

        call_args = ['ionice', '-c', '2', '-n', '7'] if ionice and (shutil.which('ionice') != None) else []
        call_args += self._call_prefix
        if parallel:
            call_args.append('-m')
        call_args.extend(['rsync', '-d', '-r', source, target])
        if not quiet:
            print(' '.join(call_args))
        check_call(call_args)

    def delete(self, recursive, parallel, filenames, quiet):
        call_args = self._call_prefix.copy()
        if parallel:
            call_args.append('-m')
        call_args.append('rm')
        if recursive:
            call_args.append('-r')
        call_args.extend(filenames)
        if not quiet:
            print(' '.join(call_args))
        check_call(call_args)

    def stat(self, filename):
        assert filename.startswith("gs://"), "Must be a GS URI!"
        is_folder = True if filename[-1]=='/' else False

        if is_folder:
            call_args = ['gsutil', '-q', 'stat', filename + '*']
        else:
            call_args = ['gsutil', '-q', 'stat', filename]

        check_call(call_args)
