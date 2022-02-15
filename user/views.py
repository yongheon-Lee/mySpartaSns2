from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import UserModel
from django.contrib.auth import get_user_model
from django.contrib import auth


# Create your views here.
def sign_in_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me) # 비밀번호까지 다 확인해 줌
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error': '이름 혹은 비밀번호를 다시 확인하세요!'})


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:
            return render(request, 'user/signup.html', {'error': '비밀번호가 다릅니다!'})
        else:
            if username == '' or password == '' or password2 == '':
                return render(request, 'user/signup.html', {'error': '이름과 비밀번호는 필수입니다!'})
                        # 사용자가 있는지 확인하는 함수?
                        # 사용자가 있는지 확인하고, 조건에 맞는 사용자를 가져온다??
            exist_user = get_user_model().objects.filter(username=username)

            if exist_user:
                return render(request, 'user/signup.html', {'error': '이미 있는 사용자입니다!'})
            else:
                                 # create_user로 만들면 pw가 hash화 됨. 그냥 save로 하면 안됨
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    if request.method == 'GET':
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


def user_follow(request, id):
    me = request.user
    clicked_user_by_me = UserModel.objects.get(id=id)
    if me in clicked_user_by_me.followee.all():
        clicked_user_by_me.followee.remove(request.user)
    else:
        clicked_user_by_me.followee.add(request.user)
    return redirect('/user')
