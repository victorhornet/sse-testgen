"""Common methods for parsing."""

PARAM_KEYWORDS = {
    "param",
    "parameter",
    "arg",
    "argument",
    "attribute",
    "key",
    "keyword",
}
RAISES_KEYWORDS = {"raises", "raise", "except", "exception"}
RETURNS_KEYWORDS = {"return", "returns"}
YIELDS_KEYWORDS = {"yield", "yields"}


class ParseError(RuntimeError):
    """Base class for all parsing related errors."""

    pass


class DocstringMeta:
    """Docstring meta information.

    Symbolizes lines in form of

        :param arg: description
        :raises ValueError: if something happens
    """

    def __init__(self, args, description):
        """Initialize self.

        :param args: list of arguments. The exact content of this variable is
                     dependent on the kind of docstring; it's used to distinguish between
                     custom docstring meta information items.
        :param description: associated docstring description.
        """
        self.args = args
        self.description = description


class DocstringParam(DocstringMeta):
    """DocstringMeta symbolizing :param metadata."""

    def __init__(self, args, description, arg_name, type_name, is_optional, default):
        """Initialize self."""
        super().__init__(args, description)
        self.arg_name = arg_name
        self.type_name = type_name
        self.is_optional = is_optional
        self.default = default


class DocstringReturns(DocstringMeta):
    """DocstringMeta symbolizing :returns or :yields metadata."""

    def __init__(self, args, description, type_name, is_generator, return_name=None):
        """Initialize self."""
        super().__init__(args, description)
        self.type_name = type_name
        self.is_generator = is_generator
        self.return_name = return_name


class DocstringRaises(DocstringMeta):
    """DocstringMeta symbolizing :raises metadata."""

    def __init__(self, args, description, type_name):
        """Initialize self."""
        super().__init__(args, description)
        self.type_name = type_name
        self.description = description


class DocstringDeprecated(DocstringMeta):
    """DocstringMeta symbolizing deprecation metadata."""

    def __init__(self, args, description, version):
        """Initialize self."""
        super().__init__(args, description)
        self.version = version
        self.description = description


class Docstring:
    """Docstring object representation."""

    def __init__(self):
        """Initialize self."""
        self.short_description = None
        self.long_description = None
        self.blank_after_short_description = False
        self.blank_after_long_description = False
        self.meta = []

    @property
    def params(self):
        return [item for item in self.meta if isinstance(item, DocstringParam)]

    @property
    def raises(self):
        return [
            item for item in self.meta if isinstance(item, DocstringRaises)
        ]

    @property
    def returns(self):
        for item in self.meta:
            if isinstance(item, DocstringReturns):
                return item
        return None

    @property
    def deprecation(self):
        for item in self.meta:
            if isinstance(item, DocstringDeprecated):
                return item
        return None
