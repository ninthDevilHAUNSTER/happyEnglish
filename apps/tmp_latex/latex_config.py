import os

TMP_LATEX_PATH = r"D:\python_box\happyEnglish\apps\tmp_latex"

LATEX_WRITER_DICT = {
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
    "WORD_PART_START": """
\\begin{flushleft}
一. 单词部分
\\end{flushleft}
""",
    "WORD_PART_DOUBLE_COLUMN_WITH_UNDERLINE": """
\\begin{multicols}{2}
\\begin{flushleft}
%s.\ %s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}

\\begin{flushleft}
%s.\ %s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}
\\end{multicols}
""",
    "WORD_PART_SINGLE_COLUMN_WITH_UNDERLINE": """
\\begin{multicols}{2}
\\begin{flushleft}
%s.\ %s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}
\\end{multicols}
""",
    "WORD_PART_DOUBLE_COLUMN_WITH_ANSWER": """
\\begin{multicols}{2}
\\begin{flushleft}
%s.\ %s \ %s
\\end{flushleft}

\\begin{flushleft}
%s.\ %s \ %s
\\end{flushleft}
\\end{multicols}
""",
    "WORD_PART_SINGLE_COLUMN_WITH_ANSWER": """
\\begin{multicols}{2}
\\begin{flushleft}
%s.\ %s \ \ \ \ \\underline{\hspace{3cm}}
\\end{flushleft}
\\end{multicols}
""",
    "SENTENCE_PART_START": """
\\begin{flushleft}
二. 句子部分
\\end{flushleft}
""",
    "SENTENCE_PART_WITH_UNDERLINE": """
\\begin{flushleft}
%s.\ %s

\\underline{\\hspace{16cm}}
\\end{flushleft}
""",
    "SENTENCE_PART_WITH_ANSWER": """
\\begin{flushleft}
%s.\ %s

%s
\\end{flushleft}
""",
    "TAIL": r"""
\end{document}
""",
}


def latex_header_gen(title="每日单词", user_name="烧包"):
    title = "".join(i + "\ " for i in list(title))
    return LATEX_WRITER_DICT['HEADER'] % (
        title,
        user_name
    )


def word_part_start():
    return LATEX_WRITER_DICT["WORD_PART_START"]


def word_part_double_column_with_underline(index1, word1, index2, word2):
    return LATEX_WRITER_DICT['WORD_PART_DOUBLE_COLUMN_WITH_UNDERLINE'] % (index1, word1, index2, word2)


def word_part_single_column_with_underline(index, word):
    return LATEX_WRITER_DICT['WORD_PART_SINGLE_COLUMN_WITH_UNDERLINE'] % (index, word)


def word_part_double_column_with_answer(index1, word1, answer1, index2, word2, answer2):
    return LATEX_WRITER_DICT['WORD_PART_DOUBLE_COLUMN_WITH_ANSWER'] % (
        index1, word1, answer1, index2, word2, answer2
    )


def word_part_single_column_with_answer(index, word, answer):
    return LATEX_WRITER_DICT['WORD_PART_SINGLE_COLUMN_WITH_ANSWER'] % (
        index, word, answer
    )


def sentence_part_start():
    return LATEX_WRITER_DICT['SENTENCE_PART_START']


def sentence_part_with_underline(index, sentence):
    return LATEX_WRITER_DICT['SENTENCE_PART_WITH_UNDERLINE'] % (
        index, sentence
    )


def sentence_part_with_answer(index, sentence, answer):
    return LATEX_WRITER_DICT['SENTENCE_PART_WITH_ANSWER'] % (
        index, sentence, answer
    )


def tail():
    return LATEX_WRITER_DICT['TAIL']


def compile_cmd(file_name):
    if "linux" in os.sys.platform:
        return "".join(i + " " for i in [
            "xelatex",
            # "-interaction=batchmode",
            # "-halt-on-error",
            file_name,
            "1>/dev/null 2>/dev/null &"])
    elif "win" in os.sys.platform:
        return "".join(i + " " for i in [
            "pdflatex",
            # "-interaction=batchmode",
            # "-halt-on-error",
            file_name,
            ">nul"])
    else:
        return False
