from nbenumerate.version import Version


def test_version():
    """Checks that the version counter behaves correctly."""
    version = Version()

    version.increment(level=1)
    assert str(version) == "1."

    version.increment(level=2)
    version.increment(level=2)
    assert str(version) == "1.2."

    version.increment(level=1)
    assert str(version) == "2."

    version.increment(level=3)
    assert str(version) == "2.0.1."
