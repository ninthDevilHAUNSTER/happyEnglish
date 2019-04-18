import os
from collections import OrderedDict

TMP_LATEX_PATH = r"D:\python_box\happyEnglish\apps\tmp_latex"
COMPILE_CMD = lambda filename: "pdflatex {} >nul".format(TMP_LATEX_PATH + filename)

LATEX_WRITER_DICT = OrderedDict(
    {
        "HEADER": r"""\documentclass[a4paper, 12pt]{article}
\usepackage[UTF8]{ctex}
\usepackage{multicol}
\usepackage{geometry}
\geometry{a4paper,left=2cm,right=2cm,top=1cm,bottom=1cm}

\begin{document}
    \noindent

    \title{ %s }
    \author{ %s }
    \maketitle
""",
        "WORD_START": """
\\begin{flushleft}
一. 单词部分
\\end{flushleft}
"""

    }
)


def latex_header_gen(title="每日单词", user_name="烧包"):
    title = "".join(i + "\ " for i in list(title))
    return LATEX_WRITER_DICT['HEADER'] % (
        title,
        user_name
    )
