from strato.commands.util import get_backend


def test_backend():
    cloud_backends = [("aws", "s3"), ("gcp", "gs")]
    for cloud_backend in cloud_backends:
        assert cloud_backend[0] == get_backend(["{}://foo".format(cloud_backend[1]), "/a/b"])
        assert cloud_backend[0] == get_backend(["{}://foo/".format(cloud_backend[1]), "/a/b"])
        assert cloud_backend[0] == get_backend(["/a/b", "{}://foo/".format(cloud_backend[1])])
