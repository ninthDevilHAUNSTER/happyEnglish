from tmp_latex.latex_config import *
import os
from datetime import datetime
import shutil
from happyEnglish import settings


def compile(words, sentences):
    os.system('del ./media/*.pdf')
    latex = HEADER
    for word_index in range(0, words.__len__(), 2):
        try:
            latex += WORD_MIDDLE_WARE % (words[word_index][0],
                                         words[word_index + 1][0])
        except IndexError:
            latex += WORD_MIDDLE_WARE % (words[word_index][0], "")

    for sentence_index in range(0, sentences.__len__()):
        latex += SENTENCE_MIDDLE_WARE % (sentences[sentence_index][0])
    latex += TAIL
    open(TMP_LATEX_PATH + "\\tmp.tex", 'w', encoding="utf8").write(latex)
    os.system(PDF_LATEX_COMPILE_CMD)
    os.remove('tmp.aux')
    os.remove('tmp.log')
    save_path = settings.MEDIA_ROOT + "\\" + datetime.strftime(datetime.now(), '%y_%m_%d_%H_%M')
    f_name = "{}.pdf".format(save_path)
    shutil.move('tmp.pdf', "{}".format(f_name))
    return f_name
