import pytest

from strato.commands import cp
from strato.tests.helpers import gsutil


def test_cp_file_aws(capsys):
    cp.main(["file1", "s3://foo/bar/", "--dryrun"])
    assert "aws s3 cp --only-show-errors file1 s3://foo/bar/\n" == capsys.readouterr().out


@pytest.fixture(scope="module", params=[True, False])
def trailing_slash(request):
    return request.param


def test_cp_dir_aws(capsys, trailing_slash):
    cp.main(["dir1", "s3://foo/bar" + ("/" if trailing_slash else ""), "-r", "--dryrun"])

    assert (
        "aws s3 cp --only-show-errors --recursive dir1/ s3://foo/bar/dir1\n"
        == capsys.readouterr().out
    )


def test_cp_file_gcp(capsys):
    cp.main(["file1", "gs://foo/bar/", "--dryrun"])
    assert gsutil + " cp file1 gs://foo/bar/\n" == capsys.readouterr().out


def test_cp_dir_gcp(capsys):
    cp.main(["dir1", "gs://foo/bar", "-r", "--dryrun"])
    assert gsutil + " cp -r dir1 gs://foo/bar\n" == capsys.readouterr().out


def test_cp_file_local(capsys):
    cp.main(["file1", "/bar/foo", "--dryrun"])
    assert "cp file1 /bar/foo\n" == capsys.readouterr().out


def test_cp_dir_local(capsys):
    cp.main(["file1", "/bar/foo", "-r", "--dryrun"])
    assert "mkdir -p /bar/foo\ncp -r file1 /bar/foo\n" == capsys.readouterr().out
