from strato.commands import rm
from strato.tests.helpers import gsutil


def test_rm_aws(capsys):
    # FIXME recursive inferred from trailing slashes
    rm.main(["s3://foo/bar", "--dryrun"])
    assert "aws s3 rm --only-show-errors s3://foo/bar\n" == capsys.readouterr().out


def test_rm_aws_recursive(capsys):
    # FIXME recursive inferred from trailing slashes
    rm.main(["s3://foo/bar/", "--dryrun"])
    assert "aws s3 rm --only-show-errors --recursive s3://foo/bar/\n" == capsys.readouterr().out


def test_rm_gcp(capsys):
    rm.main(["gs://foo/bar/", "--dryrun"])
    assert gsutil + " rm gs://foo/bar/\n" == capsys.readouterr().out


def test_rm_gcp_recursive(capsys):
    rm.main(["gs://foo/bar/", "--dryrun", "--recursive"])
    assert gsutil + " rm -r gs://foo/bar/\n" == capsys.readouterr().out


def test_rm_local(capsys):
    rm.main(["file1", "--dryrun"])
    assert "rm file1\n" == capsys.readouterr().out


def test_rm_local_recursive(capsys):
    rm.main(["file1", "--dryrun", "--recursive"])
    assert "rm -r file1\n" == capsys.readouterr().out
