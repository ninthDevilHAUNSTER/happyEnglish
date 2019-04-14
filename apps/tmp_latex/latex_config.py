import os

TMP_LATEX_PATH = r"D:\python_box\happyEnglish\apps\tmp_latex"
PDF_LATEX_COMPILE_CMD = "pdflatex {}".format(TMP_LATEX_PATH + "\\tmp.tex")

HEADER = r"""\documentclass[a4paper, 12pt]{article}
\usepackage[UTF8]{ctex}
\usepackage{multicol}
\usepackage{geometry}
\geometry{a4paper,left=2cm,right=2cm,top=1cm,bottom=1cm}

\begin{document}
    \noindent

    \title{每\ 日\ 单\ 词\ }
    \author{烧包}
    \maketitle
"""

WORD_MIDDLE_WARE = """
\\begin{multicols}{2}
\\begin{flushleft}
%s \ \ \ \ \\underline{\hspace{3cm}}
\end{flushleft}

\\begin{flushleft}
%s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}
\\end{multicols}
"""

SENTENCE_MIDDLE_WARE = """
\\begin{flushleft}
%s

\\underline{\\hspace{16cm}}
\\end{flushleft}
"""

TAIL = r"""
\end{document}
"""


def test_complie(words, sentences):
    words = ['delusion', 'grafication']
    sentence = ['In the word , two things are infinite , human\'s fool and universe, and I\'m sure what universe is .']
    LATEX = HEADER + WORD_MIDDLE_WARE % (words[0], words[1]) + SENTENCE_MIDDLE_WARE % (sentence[0]) + TAIL
    open(TMP_LATEX_PATH + "\\tmp.tex", 'w', encoding="utf8").write(LATEX)
    os.system(PDF_LATEX_COMPILE_CMD)
