from tmp_latex.latex_word_list_config import *
from tmp_latex.latex_answer_list_config import SENTENCE_ANSWER_MIDDLE_WARE, WORD_ANSWER_MIDDLE_WARE, \
    WORD_ANSWER_MIDDLE_WARE_SINGLE_CASE, PDF_LATEX_COMPILE_CMD_ANSWER, HEADER_ANSWER
from tmp_latex.latex_config import latex_header_gen
import os
from datetime import datetime
import shutil
from happyEnglish import settings


def compile_answers(words, sentences, user="匿名"):
    latex = latex_header_gen(title="每日单词答案", user_name=user)
    if words.__len__() > 0:
        latex += WORD_START

    for word_index in range(0, words.__len__(), 2):
        try:
            latex += WORD_ANSWER_MIDDLE_WARE % (str(word_index + 1), words[word_index][0], words[word_index][1],
                                                str(word_index + 2), words[word_index + 1][0], words[word_index + 1][1])
        except IndexError:
            latex += WORD_ANSWER_MIDDLE_WARE_SINGLE_CASE % (str(word_index), words[word_index][0], words[word_index][1])

    if sentences.__len__() > 0:
        latex += SENTENCE_START

    for sentence_index in range(0, sentences.__len__()):
        latex += SENTENCE_ANSWER_MIDDLE_WARE % (
            str(sentence_index + 1), sentences[sentence_index][0], sentences[sentence_index][1])
    latex += TAIL

    open(TMP_LATEX_PATH + "\\ans.tex", 'w', encoding="utf8").write(latex)
    os.system(PDF_LATEX_COMPILE_CMD_ANSWER)
    os.remove('ans.aux')
    os.remove('ans.log')
    save_path = settings.MEDIA_ROOT + "\\pdfs\\"
    f_name = datetime.strftime(datetime.now(), 'answers_%y_%m_%d_%H_%M') + ".pdf"
    shutil.move('ans.pdf', "{}".format(save_path + f_name))
    return f_name


def compile_words(words, sentences, user="匿名"):
    latex = latex_header_gen(title="每日单词", user_name=user)
    if words.__len__() > 0:
        latex += WORD_START

    for word_index in range(0, words.__len__(), 2):
        try:
            latex += WORD_MIDDLE_WARE % (str(word_index + 1), words[word_index][0],
                                         str(word_index + 2), words[word_index + 1][0])
        except IndexError:
            latex += WORD_MIDDLE_WARE_SINGLE_CASE % (str(word_index), words[word_index][0])

    if sentences.__len__() > 0:
        latex += SENTENCE_START

    for sentence_index in range(0, sentences.__len__()):
        latex += SENTENCE_MIDDLE_WARE % (str(sentence_index + 1), sentences[sentence_index][0])
    latex += TAIL

    open(TMP_LATEX_PATH + "\\tmp.tex", 'w', encoding="utf8").write(latex)
    os.system(PDF_LATEX_COMPILE_CMD)
    os.remove('tmp.aux')
    os.remove('tmp.log')
    save_path = settings.MEDIA_ROOT + "\\pdfs\\"
    f_name = datetime.strftime(datetime.now(), 'words_%y_%m_%d_%H_%M') + ".pdf"
    shutil.move('tmp.pdf', "{}".format(save_path + f_name))
    return f_name
