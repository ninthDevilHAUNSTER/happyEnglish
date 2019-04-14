from django.shortcuts import render, render_to_response
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest
from datetime import datetime, timedelta
from .form import UploadFileForm
from happyEnglish.settings import MEDIA_ROOT
from .models import ExcelStatus, Words
from db_tools.words_input import handle_excel_file
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from tmp_latex.latex_compile import compile


# Create your views here.
def page_not_found(request):
    return render_to_response('404.html', status=404)


def bad_request(request):
    return render_to_response('500.html', status=500)


def word_import(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['xl_file']
            new_file = form.save()
            # 名称是否重复
            new_file.name = file.name
            new_file.save()
            id = ExcelStatus.objects.filter(name=file.name)[0].id
            try:
                success_or_fail, msg = handle_excel_file(id)
                print(msg)
                if success_or_fail:
                    return render(request, 'happy_recite_word/import.html',
                                  {'form': form, 'success': True, 'msg': msg})
                else:
                    ExcelStatus.objects.filter(id=id).delete()
                    return render(request, 'happy_recite_word/import.html',
                                  {'form': form, 'failure': True, 'msg': msg})

            except Exception or IndexError or ValueError as ex:
                # print(ex.args)
                ExcelStatus.objects.filter(id=id).delete()
                return render(request, 'happy_recite_word/import.html',
                              {'form': form, 'failure': True, 'msg': ex.args.__str__()})
    else:
        form = UploadFileForm()
    return render(request, 'happy_recite_word/import.html', {'form': form})


def del_excel_file(request, id):
    if request.method == "GET" and id is not None:
        Words.objects.filter(file_source_id=id).delete()
        ExcelStatus.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('home'))
    else:
        return render_to_response('500.html', status=500)


def view_excel(request, id):
    if request.method == "GET" and id is not None:
        word_list = [i for i in Words.objects.filter(file_source_id=id)]
        return render(request, 'happy_recite_word/view_excel.html', {
            'words': word_list
        })
    else:
        return render_to_response('500.html', status=500)


def word_output(request):
    return render(request, 'happy_recite_word/output.html')


from random import randint


def gen_words_list(request, id):
    ExcelStatus.objects.filter(id=id).update(recite_time=datetime.now())
    words = Words.objects.filter(file_source_id=id, word_or_sentence=1)
    sentences = Words.objects.filter(file_source_id=id, word_or_sentence=2)

    t_words = []
    t_sentences = []

    for word in words:
        if word.cn2en == 0:
            word.cn2en = randint(1, 2)

        if word.cn2en == 1:
            t_words.append((word.cn, word.en))
        elif word.cn2en == 2:
            t_words.append((word.en, word.cn))

    for sentence in sentences:
        if sentence.cn2en == 0:
            sentence.cn2en = randint(1, 2)

        if sentence.cn2en == 1:
            t_sentences.append((sentence.cn, sentence.en))
        elif sentence.cn2en == 2:
            t_sentences.append((sentence.en, sentence.en))

    f_name = compile(t_words, t_sentences)
    with open(f_name, 'rb') as pdfExtract:
        response = HttpResponse(pdfExtract.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            datetime.strftime(datetime.now(), '%y_%m_%d_%H_%M') + ".pdf"
        )
        return response


def word_management(request):
    full_files = ExcelStatus.objects.all()
    paginator = Paginator(full_files, 5)
    page = request.GET.get('page')
    files = paginator.get_page(page)
    return render(request, 'happy_recite_word/management.html', {'files': files})


def index(request):
    # get datetime
    # SELECT ID FROM EXCELES WHERE RECITE_TIME< NOW() AND RECITE_TIME > NOW() - 24 hours
    ls = ExcelStatus.objects.filter(
        Q(recite_time__lt=datetime.now()) & Q(recite_time__gt=datetime.now() - timedelta(hours=24)))
    if ls.__len__() >= 1:
        return render(request, 'happy_recite_word/home.html', {'beilema': True})
    else:
        return render(request, 'happy_recite_word/home.html', {'beilema': False})
