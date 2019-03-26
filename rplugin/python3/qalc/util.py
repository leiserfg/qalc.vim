import re

_ansi_re = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def ansi_escape(text):
    return _ansi_re.sub("", text)
