from django.shortcuts import render, redirect

# Create your views here.
from .forms import *
from .models import *
import datetime

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
