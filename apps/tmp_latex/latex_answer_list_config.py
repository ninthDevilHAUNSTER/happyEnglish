import os

TMP_LATEX_PATH = r"D:\python_box\happyEnglish\apps\tmp_latex"
PDF_LATEX_COMPILE_CMD_ANSWER = "pdflatex  {}  >nul".format(TMP_LATEX_PATH + "\\ans.tex")

HEADER_ANSWER = r"""\documentclass[a4paper, 12pt]{article}
\usepackage[UTF8]{ctex}
\usepackage{multicol}
\usepackage{geometry}
\geometry{a4paper,left=2cm,right=2cm,top=1cm,bottom=1cm}

\begin{document}
    \noindent

    \title{每\ 日\ 单\ 词\ 答\ 案\ }
    \author{烧包}
    \maketitle
"""

WORD_START = """
\\begin{flushleft}
一. 单词部分
\\end{flushleft}
"""

WORD_ANSWER_MIDDLE_WARE = """
\\begin{multicols}{2}
\\begin{flushleft}
%s.\ %s \ %s
\\end{flushleft}

\\begin{flushleft}
%s.\ %s \ %s
\\end{flushleft}
\\end{multicols}
"""

WORD_ANSWER_MIDDLE_WARE_SINGLE_CASE = """
\\begin{multicols}{2}
\\begin{flushleft}
%s.\ %s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}
\\end{multicols}
"""

SENTENCE_START = """
二. 单词部分
"""

SENTENCE_ANSWER_MIDDLE_WARE = """
\\begin{flushleft}
%s.\ %s

%s
\\end{flushleft}
"""

TAIL = r"""
\end{document}
"""


def test_complie(words, sentences):
    words = [('delusion', '幻觉'), ('grafication', '满意的')]
    sentence = [
        ('In the word , two things are infinite , human\'s fool and universe, and I\'m sure what universe is .',
         '这个世界上，有两个东西是无限的，人类的愚蠢和宇宙，而我知道，宇宙是什么')]
    LATEX = HEADER + WORD_ANSWER_MIDDLE_WARE % (
        "1", words[0][0], words[0][1], "2", words[1][0], words[1][1]) + SENTENCE_ANSWER_MIDDLE_WARE % (
                "1", sentence[0][0], sentence[0][1]) + TAIL
    open(TMP_LATEX_PATH + "\\tmp.tex", 'w', encoding="utf8").write(LATEX)
    os.system(PDF_LATEX_COMPILE_CMD_ANSWER)


if __name__ == '__main__':
    test_complie(1, 1)
