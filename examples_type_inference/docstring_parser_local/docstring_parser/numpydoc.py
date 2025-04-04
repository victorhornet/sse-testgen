"""Numpydoc-style docstring parsing.

.. seealso:: https://numpydoc.readthedocs.io/en/latest/format.html
"""

import inspect
import itertools
import re

from .common import (
    Docstring,
    DocstringDeprecated,
    DocstringMeta,
    DocstringParam,
    DocstringRaises,
    DocstringReturns,
)


def _pairwise(iterable, end=None):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.zip_longest(a, b, fillvalue=end)


def _clean_str(string):
    string = string.strip()
    if len(string) > 0:
        return string


KV_REGEX = re.compile(r"^[^\s].*$", flags=re.M)

PARAM_KEY_REGEX = re.compile(r"^(?P<name>.*?)(?:\s*:\s*(?P<type>.*?))?$")

PARAM_OPTIONAL_REGEX = re.compile(r"(?P<type>.*?)(?:, optional|\(optional\))$")

# numpydoc format has no formal grammar for this,
# but we can make some educated guesses...
PARAM_DEFAULT_REGEX = re.compile(
    r"[Dd]efault(?: is | = |: |s to |)\s*(?P<value>[\w\-\.]+)"
)

RETURN_KEY_REGEX = re.compile(r"^(?:(?P<name>.*?)\s*:\s*)?(?P<type>.*?)$")


class Section:
    """Numpydoc section parser.

    :param title: section title. For most sections, this is a heading like
                  "Parameters" which appears on its own line, underlined by
                  en-dashes ('-') on the following line.
    :param key: meta key string. In the parsed ``DocstringMeta`` instance this
                will be the first element of the ``args`` attribute list.
    """

    def __init__(self, title, key):
        self.title = title
        self.key = key

    @property
    def title_pattern(self):
        """Regular expression pattern matching this section's header.

        This pattern will match this instance's ``title`` attribute in
        an anonymous group.
        """
        return r"^({})\s*?\n{}\s*$".format(self.title, "-" * len(self.title))

    def parse(self, text):
        """Parse ``DocstringMeta`` objects from the body of this section.

        :param text: section body text. Should be cleaned with
                     ``inspect.cleandoc`` before parsing.
        """
        yield DocstringMeta([self.key], description=_clean_str(text))


class _KVSection(Section):
    """Base parser for numpydoc sections with key-value syntax.

    E.g. sections that look like this:
        key
            value
        key2 : type
            values can also span...
            ... multiple lines
    """

    def _parse_item(self, key, value):
        pass

    def parse(self, text):
        for match, next_match in _pairwise(KV_REGEX.finditer(text)):
            start = match.end()
            end = next_match.start() if next_match is not None else None
            value = text[start:end]
            yield self._parse_item(
                key=match.group(), value=inspect.cleandoc(value)
            )


class _SphinxSection(Section):
    """Base parser for numpydoc sections with sphinx-style syntax.

    E.g. sections that look like this:
        .. title:: something
            possibly over multiple lines
    """

    @property
    def title_pattern(self):
        return r"^\.\.\s*({})\s*::".format(self.title)


class ParamSection(_KVSection):
    """Parser for numpydoc parameter sections.

    E.g. any section that looks like this:
        arg_name
            arg_description
        arg_2 : type, optional
            descriptions can also span...
            ... multiple lines
    """

    def _parse_item(self, key, value):
        m = PARAM_KEY_REGEX.match(key)
        arg_name = type_name = is_optional = None
        if m is not None:
            arg_name, type_name = m.group("name"), m.group("type")
            if type_name is not None:
                optional_match = PARAM_OPTIONAL_REGEX.match(type_name)
                if optional_match is not None:
                    type_name = optional_match.group("type")
                    is_optional = True
                else:
                    is_optional = False

        default = None
        if len(value) > 0:
            default_match = PARAM_DEFAULT_REGEX.search(value)
            if default_match is not None:
                default = default_match.group("value")

        return DocstringParam(
            args=[self.key, arg_name],
            description=_clean_str(value),
            arg_name=arg_name,
            type_name=type_name,
            is_optional=is_optional,
            default=default,
        )


class RaisesSection(_KVSection):
    """Parser for numpydoc raises sections.

    E.g. any section that looks like this:
        ValueError
            A description of what might raise ValueError
    """

    def _parse_item(self, key, value):
        return DocstringRaises(
            args=[self.key, key],
            description=_clean_str(value),
            type_name=key if len(key) > 0 else None,
        )


class ReturnsSection(_KVSection):
    """Parser for numpydoc raises sections.

    E.g. any section that looks like this:
        return_name : type
            A description of this returned value
        another_type
            Return names are optional, types are required
    """

    is_generator = False

    def _parse_item(self, key, value):
        m = RETURN_KEY_REGEX.match(key)
        if m is not None:
            return_name, type_name = m.group("name"), m.group("type")
        else:
            return_name = type_name = None

        return DocstringReturns(
            args=[self.key],
            description=_clean_str(value),
            type_name=type_name,
            is_generator=self.is_generator,
            return_name=return_name,
        )


class YieldsSection(ReturnsSection):
    """Parser for numpydoc generator "yields" sections."""

    is_generator = True


class DeprecationSection(_SphinxSection):
    """Parser for numpydoc "deprecation warning" sections."""

    def parse(self, text):
        version, desc, *_ = text.split(sep="\n", maxsplit=1) + [None, None]

        if desc is not None:
            desc = _clean_str(inspect.cleandoc(desc))

        yield DocstringDeprecated(
            args=[self.key], description=desc, version=_clean_str(version),
        )


DEFAULT_SECTIONS = [
    ParamSection("Parameters", "param"),
    ParamSection("Params", "param"),
    ParamSection("Arguments", "param"),
    ParamSection("Args", "param"),
    ParamSection("Other Parameters", "other_param"),
    ParamSection("Other Params", "other_param"),
    ParamSection("Other Arguments", "other_param"),
    ParamSection("Other Args", "other_param"),
    ParamSection("Receives", "receives"),
    ParamSection("Receive", "receives"),
    RaisesSection("Raises", "raises"),
    RaisesSection("Raise", "raises"),
    RaisesSection("Warns", "warns"),
    RaisesSection("Warn", "warns"),
    ParamSection("Attributes", "attribute"),
    ParamSection("Attribute", "attribute"),
    ReturnsSection("Returns", "returns"),
    ReturnsSection("Return", "returns"),
    YieldsSection("Yields", "yields"),
    YieldsSection("Yield", "yields"),
    Section("Examples", "examples"),
    Section("Example", "examples"),
    Section("Warnings", "warnings"),
    Section("Warning", "warnings"),
    Section("See Also", "see_also"),
    Section("Related", "see_also"),
    Section("Notes", "notes"),
    Section("Note", "notes"),
    Section("References", "references"),
    Section("Reference", "references"),
    DeprecationSection("deprecated", "deprecation"),
]


class NumpydocParser:
    def __init__(self, sections=None):
        """Setup sections.

        :param sections: Recognized sections or None to defaults.
        """
        sections = sections or DEFAULT_SECTIONS
        self.sections = {s.title: s for s in sections}
        self._setup()

    def _setup(self):
        self.titles_re = re.compile(
            r"|".join(s.title_pattern for s in self.sections.values()),
            flags=re.M,
        )

    def add_section(self, section):
        """Add or replace a section.

        :param section: The new section.
        """

        self.sections[section.title] = section
        self._setup()

    def parse(self, text):
        """Parse the numpy-style docstring into its components.

        :returns: parsed docstring
        """
        ret = Docstring()
        if not text:
            return ret

        # Clean according to PEP-0257
        text = inspect.cleandoc(text)

        # Find first title and split on its position
        match = self.titles_re.search(text)
        if match:
            desc_chunk = text[: match.start()]
            meta_chunk = text[match.start() :]
        else:
            desc_chunk = text
            meta_chunk = ""

        # Break description into short and long parts
        parts = desc_chunk.split("\n", 1)
        ret.short_description = parts[0] or None
        if len(parts) > 1:
            long_desc_chunk = parts[1] or ""
            ret.blank_after_short_description = long_desc_chunk.startswith(
                "\n"
            )
            ret.blank_after_long_description = long_desc_chunk.endswith("\n\n")
            ret.long_description = long_desc_chunk.strip() or None

        for match, nextmatch in _pairwise(self.titles_re.finditer(meta_chunk)):
            title = next(g for g in match.groups() if g is not None)
            factory = self.sections[title]

            # section chunk starts after the header,
            # ends at the start of the next header
            start = match.end()
            end = nextmatch.start() if nextmatch is not None else None
            ret.meta.extend(factory.parse(meta_chunk[start:end]))

        return ret


def parse(text):
    """Parse the numpy-style docstring into its components.

    :returns: parsed docstring
    """
    return NumpydocParser().parse(text)