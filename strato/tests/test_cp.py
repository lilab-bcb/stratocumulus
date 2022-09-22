from strato.commands import cp
from strato.tests.helpers import gsutil


def test_cp_file_aws(capsys):
    cp.main(["file1", "s3://foo/bar/", "--dryrun"])
    assert "aws s3 cp --only-show-errors file1 s3://foo/bar/\n" == capsys.readouterr().out


def test_cp_dir_aws(capsys):
    # FIXME Local path must have slash for recursive copy. Recursive flag ignored
    cp.main(["file1/", "s3://foo/bar", "--dryrun"])
    assert (
        "aws s3 cp --only-show-errors --recursive file1/ s3://foo/bar/\n" == capsys.readouterr().out
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
