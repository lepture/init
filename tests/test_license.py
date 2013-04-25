
from init import license


def test_licenses():
    assert 'bsd3' in license.licenses()
    assert 'mit' in license.licenses()


def test_read():
    assert license.read('unknown') is None
    assert 'MIT' in license.read('mit')
    assert 'MIT' in license.read('mit.txt')


def test_parse():
    assert license.parse('unknown') is None
    assert '{{ year }}' in license.parse('mit')
    assert '{{ year }}' not in license.parse('mit', year=2013)
