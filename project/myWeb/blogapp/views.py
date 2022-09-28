from xmlrpc.client import boolean
from django.shortcuts import render, redirect
from django.http import Http404

from django.contrib import messages

from .forms import *
from .models import *
import datetime

from .forms import FileUploadForm
from .models import FileUpload

from django.core.paginator import Paginator

from django.http import HttpResponse
import os
from django.conf import settings
import mimetypes
import urllib

import jpype

from pathlib import Path

def board(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        board = Board(
            title=title,
            content=content,
            user=user,
            username=user.username
        )
        board.save()
        return redirect('board')
    else:
        boardForm = BoardForm
        if(request.GET.get('q')):
            board = search(request)
        else:
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
    if board.user == request.user:
        board.delete()
        return redirect('board')
    else:
        messages.warning(request, "삭제 권한이 없습니다.")
        return redirect('board')

def boardDetail(request, pk):
    try:
        board = Board.objects.get(id=pk)
    except:
        raise Http404('Not found page')
    return render(request, 'board_detail.html', {'board':board})

def file(request):
    if(request.GET.get('q')):
        fileupload = searchFile(request)
    else:
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
            type = request.FILES["imgfile"].content_type #TT
            user = request.user
            fileupload = FileUpload(
                title=title,
                content=content,
                imgfile=img,
                user=user,
                username=user.username
            )
            fileupload.save()
            encrypt(fileupload.imgfile.name)
            #messages.warning(request, "D:\web\project\myWeb\media\\" + fileupload.imgfile.name)
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
    if fileupload.user == request.user:
        fileupload.delete()
        return redirect('file')
    else:
        messages.warning(request, "삭제 권한이 없습니다.")
        return redirect('file')

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

from django.db.models import Q

def search(request):
    search_keyword = request.GET.get('q', '')
    search_type = request.GET.get('type', '')
    board = Board.objects.order_by('-id') 
    if search_keyword :
        if search_type == 'all':
            search_board_list = board.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (username__icontains=search_keyword))
        elif search_type == 'title_content':
            search_board_list = board.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
        elif search_type == 'title':
            search_board_list = board.filter(title__icontains=search_keyword)    
        elif search_type == 'content':
            search_board_list = board.filter(content__icontains=search_keyword)    
        elif search_type == 'writer':
            search_board_list = board.filter(username__icontains=search_keyword)
        return search_board_list
    return board

def searchFile(request):
    search_keyword = request.GET.get('q', '')
    search_type = request.GET.get('type', '')
    board = FileUpload.objects.order_by('-id') 
    if search_keyword :
        if search_type == 'all':
            search_board_list = board.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (username__icontains=search_keyword))
        elif search_type == 'title_content':
            search_board_list = board.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
        elif search_type == 'title':
            search_board_list = board.filter(title__icontains=search_keyword)    
        elif search_type == 'content':
            search_board_list = board.filter(content__icontains=search_keyword)    
        elif search_type == 'writer':
            search_board_list = board.filter(username__icontains=search_keyword)
        return search_board_list
    return board

def encrypt(file):
    srcFile = "D:\web\project\myWeb\media\\" + file
    #dstFile = "D:\web\project\myWeb\temp\\" + file
    #srcFile="c:/softcamp/03_Sample/test.xlsx"
    dstFile = "c:/softcamp/03_Sample/test_Enc.jpg"
    
    classpath = 'D:\web\project\myWeb\servicelinker\scsl.jar'

    jpype.startJVM(
        jpype.getDefaultJVMPath(),
        "-Djava.class.path={classpath}".format(classpath=classpath),
        convertStrings=True,
        )

    jpype.addClassPath("D:\web\project\myWeb\servicelinker\scsl.jar")
    
    jpkg = jpype.JPackage('SCSL')
    SLDsFile = jpkg.SLDsFile()

    SLDsFile.SettingPathForProperty("D:\web\project\myWeb\servicelinker\softcamp.properties")
    
    SLDsFile.SLDsInitDAC();                                                 
    SLDsFile.SLDsAddUserDAC("SECURITYDOMAIN", "111001100", 0, 0, 0)

    SLDsFile.SLDsEncFileDACV2("c:/softcamp/04_KeyFile/keyDAC_SVR0.sc", "System", srcFile, dstFile, 1)
    

def decrypt():
    return 0