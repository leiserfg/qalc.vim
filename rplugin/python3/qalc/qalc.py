import re
from subprocess import PIPE, run
from .util import ansi_escape

_comment_re = re.compile("#.*$", re.MULTILINE)
_prompt_or_empty_re = re.compile("^(>.*|\s+)$", re.MULTILINE)


def clean_input(input):
    lines = ((i, _comment_re.sub("", line)) for i, line in enumerate(input) if line)
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
            yield ansi_escape(line)


def process(input):
    idxs, text = clean_input(input)
    output = qalc(text)
    return zip(idxs, clean_output(output))


def main():
    text = """
    343 + 3434
    33 + sin(12)

    12USD to EUR
    asdfasdf  #adsfasdf
    """
    print("\n".join(f"{id} {val}" for id, val in process(text)))


if __name__ == "__main__":
    main()
