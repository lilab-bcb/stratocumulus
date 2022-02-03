import os, shutil
import boto3
from subprocess import check_call, CalledProcessError
from typing import Optional

def parse_wildcard(filepath):
    fp_list = filepath[5:].split('/')
    wd_idx = -1
    for i in range(len(fp_list)):
        if '*' in fp_list[i]:
            wd_idx = i
            break
    assert wd_idx != -1, "The given path doesn't contain wildcard!"

    parent_folder = "s3://" + '/'.join(fp_list[0:wd_idx])
    wildcard = '/'.join(fp_list[wd_idx:])

    return parent_folder, wildcard

class AWSBackend:
    def __init__(self):
        self._backend = 'aws'
        self._call_prefix = ['aws', 's3']

    def copy(self, ionice, filenames, profile, quiet):
        call_args = ['ionice', '-c', '2', '-n', '7'] if ionice and (shutil.which('ionice') != None) else []
        call_args += self._call_prefix
        call_args.extend(['cp', '--only-show-errors'])
        if profile is not None:
            call_args.extend(['--profile', profile])

        source_files = filenames[:-1]
        target = filenames[-1]
        if len(source_files) > 1 and target[-1] != '/':
            target += '/'

        # Copy files one by one.
        for source in source_files:
            subcall_args = call_args.copy()
            subcall_target = target
            if ('*' in source) and (source.startswith('s3://')): # S3 URI containing wildcards
                parent_folder, wildcard = parse_wildcard(source)
                subcall_args.extend(['--recursive', '--include', f"\"{wildcard}\""])
                source = parent_folder + '/'
            elif source[-1] == '/': # copy an S3 folder
                subcall_args.append('--recursive')
                if subcall_target[-1] != '/':
                    subcall_target = subcall_target + '/' + os.path.basename(source)
                else:
                    subcall_target = subcall_target + os.path.basename(source)
            subcall_args.extend([source, subcall_target])
            if not quiet:
                print(' '.join(subcall_args))
            check_call(subcall_args)

    def sync(self, ionice, source, target, profile, quiet):
        call_args = ['ionice', '-c', '2', '-n', '7'] if ionice and (shutil.which('ionice') != None) else []
        call_args += self._call_prefix
        if profile is not None:
            call_args.extend(['--profile', profile])
        call_args.extend(['sync', '--delete', '--only-show-errors', source, target])
        if not quiet:
            print(' '.join(call_args))
        check_call(call_args)

    def delete(self, filenames, profile, quiet):
        call_args = self._call_prefix.copy()
        call_args.extend(['rm', '--only-show-errors'])

        if profile is not None:
            call_args.extend(['--profile', profile])

        # Delete files one by one.
        for f in filenames:
            subcall_args = call_args.copy()
            if f[-1] == '/':
                subcall_args.append('--recursive')
            subcall_args.append(f)
            if not quiet:
                print(' '.join(subcall_args))
            check_call(subcall_args)

    def stat(self, filename, profile):
        assert filename.startswith("s3://"), "Must be an S3 URI!"

        call_args = self._call_prefix.copy()
        is_folder = True if filename[-1]=='/' else False

        if is_folder:
            fn_list = filename[5:].split('/')
            bucket = fn_list[0]
            folder = '/'.join(fn_list[1:]) if len(fn_list) > 1 else ""
            session = boto3.Session(profile_name=profile)
            resp = session.client('s3').list_objects_v2(
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
            if profile is not None:
                call_args.extend(['--profile', profile])
            check_call(call_args)
