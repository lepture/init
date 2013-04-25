from nose.tools import raises
from init.template import Template


@raises(ValueError)
def test_no_value():
    return Template()


def test_dict_value():
    t = Template('hello {{foo.bar}}')
    assert t.render(foo={'bar': 'baz'}) == 'hello baz'
    assert t.render(foo='foo') == 'hello {{foo.bar}}'


def test_attr_value():
    t = Template('hello {{foo.bar}}')

    class Foo(object):
        def __init__(self):
            self.bar = 'baz'

    assert t.render(foo=Foo()) == 'hello baz'
