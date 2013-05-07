import os
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
    t = Template('hello {{foo.bar.bar}}')

    class Foo(object):
        def __init__(self, bar):
            self.bar = bar

    foo = Foo(Foo('baz'))
    assert t.render(foo=foo) == 'hello baz'

    t = Template('hello {{foo.bar.baz}}')
    assert t.render(foo=foo) == 'hello {{foo.bar.baz}}'


def test_write():
    t = Template('hello {{foo.bar}}')
    t.write('tmp/test_write.txt', foo={'bar': 'baz'})
    assert os.path.exists('tmp/test_write.txt')
    os.remove('tmp/test_write.txt')
    os.rmdir('tmp')
