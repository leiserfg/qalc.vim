import re
from functools import reduce
from subprocess import PIPE, run

from .util import ansi_escape

_comment_re = re.compile("\s*#.*$", re.MULTILINE)
_label_re = re.compile("^.*:", re.MULTILINE)

_prompt_or_empty_re = re.compile("^(>.*|\s+)$", re.MULTILINE)
_translate = [("deg", "°"), (" USD", "$"), (" EUR", "€"), (" GBP", "£"), (" JPY", "¥")]


def clean_input(input):
    uncommented_lines = (_comment_re.sub("", line) for line in input)
    uncommented_lines = (_label_re.sub("", line) for line in uncommented_lines)
    lines = (
        (i, l) for i, l in enumerate(uncommented_lines) if l
    )  # clear empty lines and comment lines
    idxs = []
    new_text = []
    for i, l in lines:
        idxs.append(i)
        new_text.append(l)
    return idxs, "\n".join(new_text)


def qalc(text):
    p = run(["qalc", "-t"], stdout=PIPE, input=text, encoding="utf-8")
    return p.stdout


def clean_output(output):
    without_prompt = _prompt_or_empty_re.sub("", output)
    for line in without_prompt.splitlines():
        if line:
            without_ansi = ansi_escape(line)
            formated = reduce(
                lambda val, x: val.replace(x[0], x[1]), _translate, without_ansi
            )
            yield formated.strip()


def process(input):
    idxs, text = clean_input(input)
    output = qalc(text)
    return zip(idxs, clean_output(output))
