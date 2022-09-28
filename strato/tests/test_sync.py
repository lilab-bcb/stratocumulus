from strato.commands import sync
from strato.tests.helpers import gsutil


def test_sync_aws(capsys):
    sync.main(["file1", "s3://foo/bar/", "--dryrun"])
    assert (
        "aws s3 sync --delete --only-show-errors file1 s3://foo/bar/\n" == capsys.readouterr().out
    )


def test_sync_gcp(capsys):
    sync.main(["file1", "gs://foo/bar/", "--dryrun"])
    assert gsutil + " rsync -d -r file1 gs://foo/bar/\n" == capsys.readouterr().out


def test_sync_local(capsys):
    sync.main(["file1", "/bar/foo", "--dryrun"])
    assert "rsync -r --delete file1 /bar\n" == capsys.readouterr().out
