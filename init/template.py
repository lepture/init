# coding: utf-8

import os
import re


class Template(object):
    """
    Template for simpler string substitutions.

    Usage can be simple::

        >>> t = Template('hello {{foo.bar}}')
        >>> t.render(foo={'bar': 'baz'})
    """

    def __init__(self, template=None, filepath=None):
        if filepath and not template:
            f = open(filepath)
            template = f.read()
            f.close()

        if template is None:
            raise ValueError('Template is required.')

        self.template = template

    def _value(self, key, data):
        bits = None

        if isinstance(key, list):
            bits = key
        elif '.' in key:
            bits = key.split('.')

        if bits and len(bits) == 1:
            key = bits[0]
            bits = None

        if not bits:
            if isinstance(data, dict) and key in data:
                return data[key]
            if hasattr(data, key):
                return getattr(data, key)
            return None

        if isinstance(data, dict) and bits[0] in data:
            return self._value(bits[1:], data[bits[0]])
        elif hasattr(data, bits[0]):
            return self._value(bits[1:], getattr(data, bits[0]))
        return None

    def render(self, **kwargs):
        """
        Render the template to string.
        """
        regex = re.compile(r'\{\{\s*(\S+)?\s*\}\}')

        def repl(m):
            pattern = m.group(0)
            key = m.group(1)
            value = self._value(key, kwargs)
            return str(value or pattern)

        return regex.sub(repl, self.template)

    def write(self, filepath, **kwargs):
        """
        Write the rendered results to a file.
        """

        content = self.render(**kwargs)

        folder = os.path.dirname(filepath)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        f = open(filepath, 'wb')
        f.write(content)
        f.close()
        return content
