import os

from strato.commands import cp
from strato.tests.helpers import gsutil


def test_cp_file_aws(capsys):
    cp.main(["file1", "s3://foo/bar/", "--dryrun"])
    assert "aws s3 cp --only-show-errors file1 s3://foo/bar/\n" == capsys.readouterr().out


def test_cp_dir_aws(capsys):
    # If local path ends with slash, perform recursive copy. Recursive flag ignored
    cp.main(["file1/", "s3://foo/bar", "--dryrun"])
    assert (
        "aws s3 cp --only-show-errors --recursive file1/ s3://foo/bar/\n" == capsys.readouterr().out
    )


def test_cp_dir_aws_local_dir(tmp_path, capsys):
    # Local directory exists without trailing slash-perform recursive copy
    local_dir = str(tmp_path / "file1")
    os.mkdir(local_dir)
    cp.main([local_dir, "s3://foo/bar", "--dryrun"])
    assert (
        "aws s3 cp --only-show-errors --recursive " + local_dir + "/ s3://foo/bar/\n"
        == capsys.readouterr().out
    )


def test_cp_file_gcp(capsys):
    cp.main(["file1", "gs://foo/bar/", "--dryrun"])
    assert gsutil + " cp file1 gs://foo/bar/\n" == capsys.readouterr().out


def test_cp_dir_gcp(capsys):
    cp.main(["file1", "gs://foo/bar", "-r", "--dryrun"])
    assert gsutil + " cp -r file1 gs://foo/bar\n" == capsys.readouterr().out


def test_cp_file_local(capsys):
    # FIXME only the parent directory should be created
    cp.main(["file1", "/bar/foo", "--dryrun"])
    assert "mkdir -p /bar/foo\ncp file1 /bar/foo\n" == capsys.readouterr().out
