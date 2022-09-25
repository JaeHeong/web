from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from blogapp.models import Board, FileUpload

from django.contrib import messages

# Create your views here.
# 회원가입
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            if get_user_model().objects.filter(username=request.POST['username']).first() != None:
                messages.warning(request, "같은 아이디가 존재합니다.")
                return redirect('/accounts/home/signup/')
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            auth.login(request, user)
            messages.success(request, "회원가입 성공!")
            return redirect('/')
        messages.warning(request, "비밀번호와 확인 비밀번호가 다릅니다.")
        return render(request, 'signup.html')
    return render(request, 'signup.html')

# 로그인
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('board')
        else:
            messages.warning(request, "로그인 실패.")
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('home')

# 회원탈퇴
def leave(request):
    try:
        FileUpload.objects.filter(user_id = request.user.id).delete()
        Board.objects.filter(user_id = request.user.id).delete()
        request.user.delete()
        logout(request)
        messages.success(request, "회원탈퇴가 완료되었습니다.")
        return redirect('/accounts/home/login/')
    except:
        messages.warning(request, "회원탈퇴가 실패하였습니다.")
        return redirect('/')

# home
def home(request):
    return render(request, 'home.html')