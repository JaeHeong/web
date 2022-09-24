from django.shortcuts import render, redirect

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
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.user = request.user
        board.save()
        return redirect('board')

    else:
        boardForm = BoardForm
        return render(request, 'update.html', {'boardForm':boardForm})

def boardDelete(request, pk):
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('board')

def boardDetail(request, pk):
    board = Board.objects.get(id=pk)
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
        title = request.POST['title']
        content = request.POST['content']
        img = request.FILES["imgfile"]
        user = request.user
        fileupload = FileUpload(
            title=title,
            content=content,
            imgfile=img,
            user=user,
        )
        fileupload.save()
        return redirect('file')
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)

def fileUploadDetail(request, pk):
    fileupload = FileUpload.objects.get(id=pk)
    return render(request, 'file_detail.html', {'fileupload':fileupload})

def fileEdit(request, pk):
    fileupload = FileUpload.objects.get(id=pk)
    if request.method == "POST":
        fileupload.title = request.POST['title']
        fileupload.content = request.POST['content']
        fileupload.user = request.user
        fileupload.imgfile = request.FILES['imgfile']
        fileupload.save()
        return redirect('file')

    else:
        fileuploadForm = FileUploadForm
        return render(request, 'file_update.html', {'fileuploadForm':fileuploadForm})

def fileDelete(request, pk):
    fileupload = FileUpload.objects.get(id=pk)
    fileupload.delete()
    return redirect('file')