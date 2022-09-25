from django.shortcuts import render, redirect
from django.http import Http404

from django.contrib import messages

from .forms import *
from .models import *
import datetime

from .forms import FileUploadForm
from .models import FileUpload

from django.core.paginator import Paginator

def board(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        board = Board(
            title=title,
            content=content,
            user=user,
        )
        board.save()
        return redirect('board')
    else:
        boardForm = BoardForm
        board = Board.objects.all()
        page = request.GET.get('page', '1')
        paginator = Paginator(board, '10')
        page_obj = paginator.get_page(page)
        context = {
            'boardForm': boardForm,
            'board': page_obj,
        }
        return render(request, 'board.html', context)

def boardEdit(request, pk):
    board = Board.objects.get(id=pk)
    if request.method == "POST":
        if board.user == request.user:
            board.title = request.POST['title']
            board.content = request.POST['content']
            board.save()
            return redirect('board')
        else:
            messages.warning(request, "수정 권한이 없습니다.")
            return redirect('board')
    else:
        boardForm = BoardForm
        return render(request, 'update.html', {'boardForm':boardForm})

def boardDelete(request, pk):
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('board')

def boardDetail(request, pk):
    try:
        board = Board.objects.get(id=pk)
    except:
        raise Http404('Not found page')
    return render(request, 'board_detail.html', {'board':board})

def file(request):
    fileupload = FileUpload.objects.all()
    page = request.GET.get('page', '1')
    paginator = Paginator(fileupload, '10')
    page_obj = paginator.get_page(page)
    context = {
        'fileupload': page_obj,
    }
    return render(request, 'file_board.html', context)

def fileUpload(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            content = request.POST['content']
            img = request.FILES["imgfile"]
            type = request.FILES["imgfile"].content_type
            user = request.user
            fileupload = FileUpload(
                title=title,
                content=content,
                imgfile=img,
                user=user,
            )
            fileupload.save()
            return redirect('file')
        except:
            messages.warning(request, "파일을 첨부해주세요.")
            return redirect('/fileupload')
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)

def fileUploadDetail(request, pk):
    try:
        fileupload = FileUpload.objects.get(id=pk)
    except:
        raise Http404('Not found page')
    return render(request, 'file_detail.html', {'fileupload':fileupload})

def fileEdit(request, pk):
    fileupload = FileUpload.objects.get(id=pk)
    if request.method == "POST":
        try:
            if fileupload.user == request.user:
                fileupload.title = request.POST['title']
                fileupload.content = request.POST['content']
                fileupload.imgfile = request.FILES['imgfile']
                type = request.FILES["imgfile"].content_type
                fileupload.save()
                return redirect('file')
            else:
                messages.warning(request, "수정 권한이 없습니다.")
                return redirect('file')
        except:
            messages.warning(request, "파일을 첨부해주세요.")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        fileuploadForm = FileUploadForm
        return render(request, 'file_update.html', {'fileuploadForm':fileuploadForm})

def fileDelete(request, pk):
    fileupload = FileUpload.objects.get(id=pk)
    fileupload.delete()
    return redirect('file')

from django.http import HttpResponse
import os
from django.conf import settings
import mimetypes
import urllib


def fileDownload(request):
    path = request.GET['path']
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    file_name = urllib.parse.quote(request.GET['path'].encode('utf-8'))
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % file_name
            return response
    else:
        messages.warning(request, "다운로드 할 수 없습니다.")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))