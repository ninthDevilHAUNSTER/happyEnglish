import os

TMP_LATEX_PATH = r"D:\python_box\happyEnglish\apps\tmp_latex"
PDF_LATEX_COMPILE_CMD = "pdflatex {} >nul".format(TMP_LATEX_PATH + "\\tmp.tex")

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

WORD_START = """
\\begin{flushleft}
一. 单词部分
\\end{flushleft}
"""

WORD_MIDDLE_WARE = """
\\begin{multicols}{2}
\\begin{flushleft}
%s.\ %s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}

\\begin{flushleft}
%s.\ %s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}
\\end{multicols}
"""

WORD_MIDDLE_WARE_SINGLE_CASE = """
\\begin{multicols}{2}
\\begin{flushleft}
%s.\ %s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}
\\end{multicols}
"""

SENTENCE_START = """
\\begin{flushleft}
二. 句子部分
\\end{flushleft}
"""

SENTENCE_MIDDLE_WARE = """
\\begin{flushleft}
%s.\ %s

\\underline{\\hspace{16cm}}
\\end{flushleft}
"""

TAIL = r"""
\end{document}
"""


def test_complie(words, sentences):
    words = ['delusion', 'grafication']
    sentence = ['In the word , two things are infinite , human\'s fool and universe, and I\'m sure what universe is .']
    LATEX = HEADER + WORD_MIDDLE_WARE % ("1", words[0], "2", words[1]) + SENTENCE_MIDDLE_WARE % (
        "1", sentence[0]) + TAIL
    open(TMP_LATEX_PATH + "\\tmp.tex", 'w', encoding="utf8").write(LATEX)
    os.system(PDF_LATEX_COMPILE_CMD)


if __name__ == '__main__':
    test_complie(1, 1)
