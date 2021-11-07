import os, shutil
import boto3
from subprocess import check_call, CalledProcessError


class AWSBackend:
    def __init__(self):
        self._backend = 'aws'
        self._call_prefix = ['aws', 's3']

    def copy(self, ionice, filenames):
        call_args = ['ionice', '-c', '2', '-n', '7'] if ionice and (shutil.which('ionice') != None) else []
        call_args += self._call_prefix
        call_args.extend(['cp', '--only-show-errors'])

        source_files = filenames[:-1]
        target = filenames[-1]
        if len(source_files) > 1 and target[-1] != '/':
            target += '/'

        # Copy files one by one.
        for source in source_files:
            subcall_args = call_args.copy()
            subcall_target = target
            if source[-1] == '/':
                subcall_args.append('--recursive')
                if subcall_target[-1] != '/':
                    subcall_target = subcall_target + '/' + os.path.basename(source)
                else:
                    subcall_target = subcall_target + os.path.basename(source)
            subcall_args.extend([source, subcall_target])
            print(' '.join(subcall_args))
            check_call(subcall_args)

    def sync(self, ionice, source, target):
        call_args = ['ionice', '-c', '2', '-n', '7'] if ionice and (shutil.which('ionice') != None) else []
        call_args += self._call_prefix
        call_args.extend(['sync', '--delete', '--only-show-errors', source, target])
        print(' '.join(call_args))
        check_call(call_args)

    def delete(self, filenames):
        call_args = self._call_prefix.copy()
        call_args.extend(['rm', '--only-show-errors'])

        # Delete files one by one.
        for f in filenames:
            subcall_args = call_args.copy()
            if f[-1] == '/':
                subcall_args.append('--recursive')
            subcall_args.append(f)
            print(' '.join(subcall_args))
            check_call(subcall_args)

    def stat(self, filename):
        assert filename.startswith("s3://"), "Must be an S3 URI!"

        call_args = self._call_prefix.copy()
        is_folder = True if filename[-1]=='/' else False

        if is_folder:
            fn_list = filename[5:].split('/')
            bucket = fn_list[0]
            folder = '/'.join(fn_list[1:]) if len(fn_list) > 1 else ""
            resp = boto3.client('s3').list_objects_v2(
                Bucket = bucket,
                Prefix = folder,
            )
            if resp['KeyCount'] == 0:
                raise CalledProcessError(
                    returncode=1,
                    cmd=['strato command'],
                )
        else:
            call_args.extend(['cp', '--quiet', '--dryrun', filename, '.'])
            check_call(call_args)
