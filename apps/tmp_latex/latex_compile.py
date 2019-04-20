import os
from datetime import datetime
import shutil
from happyEnglish import settings
import tmp_latex.latex_config as la
from tmp_latex.latex_config import TMP_LATEX_PATH


def dictation_paper_compiler(words, sentences, user="匿名"):
    latex = la.latex_header_gen(title="每日单词", user_name=user)
    if words.__len__() > 0:
        latex += la.word_part_start()

        for word_index in range(0, words.__len__(), 2):
            try:
                latex += la.word_part_double_column_with_underline(
                    index1=str(word_index + 1), word1=words[word_index][0],
                    index2=str(word_index + 2), word2=words[word_index + 1][0]
                )
            except IndexError:
                latex += la.word_part_single_column_with_underline(
                    index=str(word_index + 1), word=words[word_index][0]
                )
    if sentences.__len__() > 0:
        latex += la.sentence_part_start()

        for sentence_index in range(0, sentences.__len__()):
            latex += la.sentence_part_with_underline(
                index=str(sentence_index + 1), sentence=sentences[sentence_index][0]
            )
    latex += la.tail()

    open(TMP_LATEX_PATH + "\\tmp.tex", 'w', encoding="utf8").write(latex)
    os.system(la.compile_cmd(TMP_LATEX_PATH + '\\tmp.tex'))
    os.remove('tmp.aux')
    os.remove('tmp.log')
    save_path = settings.MEDIA_ROOT + "\\pdfs\\"
    f_name = datetime.strftime(datetime.now(), 'words_%y_%m_%d_%H_%M') + ".pdf"
    shutil.move('tmp.pdf', "{}".format(save_path + f_name))
    return f_name


def answer_sheet_compiler(words, sentences, user="匿名"):
    latex = la.latex_header_gen("每日单词答案", user_name=user)
    if words.__len__() > 0:
        latex += la.word_part_start()
        for word_index in range(0, words.__len__(), 2):
            try:
                latex += la.word_part_double_column_with_answer(
                    index1=str(word_index + 1), word1=words[word_index][0], answer1=words[word_index][1],
                    index2=str(word_index + 2), word2=words[word_index + 1][0], answer2=words[word_index + 1][1],
                )
            except IndexError:
                latex += la.word_part_single_column_with_answer(
                    index=str(word_index + 1), word=words[word_index][0], answer=words[word_index][1]
                )
    if sentences.__len__() > 0:
        latex += la.sentence_part_start()
        for sentence_index in range(0, sentences.__len__()):
            latex += la.sentence_part_with_answer(
                index=sentence_index, sentence=sentences[sentence_index][0], answer=sentences[sentence_index][1]
            )

    latex += la.tail()

    open(TMP_LATEX_PATH + "\\ans.tex", 'w', encoding="utf8").write(latex)
    os.system(la.compile_cmd(TMP_LATEX_PATH + '\\ans.tex'))
    os.remove('ans.aux')
    os.remove('ans.log')
    save_path = settings.MEDIA_ROOT + "\\pdfs\\"
    f_name = datetime.strftime(datetime.now(), 'answers_%y_%m_%d_%H_%M') + ".pdf"
    shutil.move('ans.pdf', "{}".format(save_path + f_name))
    return f_name


def test_compile(words, sentences):
    words = [('幻觉', 'delusion'), ('grafication', '满意的')]
    sentences = [
        ('In the word , two things are infinite , human\'s fool and universe, and I\'m sure what universe is .',
         '在这个世界，有两样东西是无限的，宇宙和人类的愚蠢，但我知道宇宙是什么')]
    dictation_paper_compiler(words, sentences)
    answer_sheet_compiler(words, sentences)


if __name__ == '__main__':
    test_compile(1, 1)
