from strato.commands import sync
from strato.tests.helpers import gcloud


def test_sync_aws(capsys):
    sync.main(["folder1", "s3://foo/bar/", "--dryrun"])
    assert (
        "aws s3 sync --delete --only-show-errors folder1 s3://foo/bar/\n" == capsys.readouterr().out
    )


def test_sync_gcp(capsys):
    sync.main(["folder1", "gs://foo/bar/", "--dryrun"])
    assert (
        gcloud + " rsync --delete-unmatched-destination-objects -r folder1 gs://foo/bar/\n"
        == capsys.readouterr().out
    )


def test_sync_local(capsys):
    sync.main(["folder1", "/bar/foo", "--dryrun"])
    assert "rsync -r --delete folder1/ /bar/foo/\n" == capsys.readouterr().out
