from django.shortcuts import render, render_to_response
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest, FileResponse
from datetime import datetime, timedelta
from .forms import UploadFileForm
from happyEnglish.settings import MEDIA_ROOT
from .models import ExcelStatus, Words
from db_tools.words_input import handle_excel_file
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from tmp_latex.latex_compile import compile_answers, compile_words
from django.views.decorators.csrf import csrf_exempt
import os
from random import randint, shuffle
from django.contrib.auth.decorators import login_required


@csrf_exempt
@login_required
def word_import(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['xl_file']
            new_file = form.save(commit=False)
            new_file.name = file.name
            new_file.owner = request.user
            new_file.save()
            e = ExcelStatus.objects.filter(name=file.name, owner=request.user)
            if not e.exists():
                return render_to_response('500.html', status=500)
            try:
                success_or_fail, msg = handle_excel_file(e[0].id)
                if success_or_fail:
                    return render(request, 'happy_recite_word/import.html',
                                  {'form': form, 'success': True, 'msg': msg})
                else:
                    ExcelStatus.objects.filter(id=e[0].id).delete()
                    return render(request, 'happy_recite_word/import.html',
                                  {'form': form, 'failure': True, 'msg': msg})

            except Exception or IndexError or ValueError as ex:
                # print(ex.args)
                ExcelStatus.objects.filter(id=e[0].id).delete()
                return render(request, 'happy_recite_word/import.html',
                              {'form': form, 'failure': True, 'msg': ex.args.__str__()})
    else:
        form = UploadFileForm()
    return render(request, 'happy_recite_word/import.html', {'form': form})


@login_required
def del_excel_file(request, id):
    if request.method == "GET" and id is not None:
        e = ExcelStatus.objects.filter(id=id, owner=request.user)
        if not e.exists():
            return render_to_response('500.html', status=500)
        Words.objects.filter(file_source_id=id).delete()
        e.delete()
        return HttpResponseRedirect(reverse('management'))
    else:
        return render_to_response('500.html', status=500)


@login_required
def view_excel(request, id):
    if request.method == "GET" and id is not None:
        word_list = [i for i in Words.objects.filter(file_source_id=id, file_source__owner=request.user)]
        return render(request, 'happy_recite_word/view_excel.html', {
            'words': word_list
        })
    else:
        return render_to_response('500.html', status=500)


@login_required
def word_output(request, id):
    e = ExcelStatus.objects.filter(id=id, owner=request.user)
    if not e.exists():
        return render_to_response('500.html', status=500)
    e = e[0]
    if e.pdf_file.name == "None":
        return HttpResponseRedirect(reverse('management'))
    else:
        with open(e.pdf_file.path, 'rb') as pdfExtract:
            response = HttpResponse(pdfExtract.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                datetime.strftime(datetime.now(), 'words_%y_%m_%d_%H_%M') + ".pdf"
            )
        return response


@login_required
def output_ans(request, id):
    e = ExcelStatus.objects.filter(id=id, owner=request.user)
    if not e.exists():
        return render_to_response('500.html', status=500)
    e = e[0]
    if e.ans_file.name == "None":
        return HttpResponseRedirect(reverse('management'))
    else:
        with open(e.ans_file.path, 'rb') as pdfExtract:
            response = HttpResponse(pdfExtract.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(
                datetime.strftime(datetime.now(), 'ans_%y_%m_%d_%H_%M') + ".pdf"
            )
        return response


import json


@login_required
def enshrine_word(request):
    if request.GET['id'].isnumeric():
        id = int(request.GET['id'])
        try:
            # 这里你想黑就黑吧，懒得理你
            w = Words.objects.filter(id=id)
            w.update(enshrine_time=w[0].enshrine_time + 1)
            return HttpResponse(json.dumps(
                {'info': 'success'}
            ), content_type="javascript/json")
        except:
            return HttpResponse(json.dumps(
                {'info': 'fail'}
            ), content_type="javascript/json")
    else:
        return HttpResponse(json.dumps(
            {'info': 'fail'}
        ), content_type="javascript/json")


@login_required
def gen_words_list(request, id):
    e = ExcelStatus.objects.filter(id=id, owner=request.user)
    if e.__len__() == 0:
        return render_to_response('500.html', status=500)

    pdf_file = e[0].pdf_file
    if pdf_file.name != "None":
        if os.path.exists(pdf_file.path):
            os.remove(pdf_file.path)
    ans_file = e[0].ans_file
    if ans_file.name != 'None':
        if os.path.exists(ans_file.path):
            os.remove(ans_file.path)
            print("[*] REMOVE")

    e.update(recite_time=datetime.now())
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
    shuffle(t_words)
    shuffle(t_sentences)

    f_name = compile_words(t_words, t_sentences)
    a_name = compile_answers(t_words, t_sentences)

    e.update(pdf_file="pdfs\\" + f_name)
    e.update(ans_file="pdfs\\" + a_name)

    with open(MEDIA_ROOT + "\\pdfs\\" + f_name, 'rb') as pdfExtract:
        response = HttpResponse(pdfExtract.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            datetime.strftime(datetime.now(), '%y_%m_%d_%H_%M') + ".pdf"
        )
    return response


@login_required
def word_management(request):
    full_files = ExcelStatus.objects.filter(owner=request.user).order_by('id')
    paginator = Paginator(full_files, 5)
    page = request.GET.get('page')
    files = paginator.get_page(page)
    return render(request, 'happy_recite_word/management.html', {'files': files})


@login_required
def show_enshrined(request):
    if request.method == "GET":
        word_list = [i for i in Words.objects.filter(enshrine_time__gte=1, file_source__owner=request.user).order_by(
            'enshrine_time')]
        return render(request, 'happy_recite_word/enshrined_word.html', {
            'words': word_list
        })
    else:
        return render_to_response('500.html', status=500)


@login_required
def get_word_voice(request, word):
    print(word)
    response = HttpResponse(mimetype='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename=TODO'
    response['Accept-Ranges'] = 'bytes'
    response['X-Sendfile'] = "TODO"
    return response


def index(request):
    # get datetime
    # SELECT ID FROM EXCELES WHERE RECITE_TIME< NOW() AND RECITE_TIME > NOW() - 24 hours
    if request.user.is_authenticated:
        ls = ExcelStatus.objects.filter(Q(owner=request.user) &
                                        Q(recite_time__lt=datetime.now()) & Q(
            recite_time__gt=datetime.now() - timedelta(hours=24)))
        if ls.__len__() >= 1:
            return render(request, 'happy_recite_word/home.html', {'beilema': True})
        else:
            return render(request, 'happy_recite_word/home.html', {'beilema': False})
    else:
        return render(request, 'happy_recite_word/home.html')
