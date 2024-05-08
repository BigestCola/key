# user/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .permissions import IsAdmin, IsAgent, IsSuperior
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SubordinateForm
from django.utils import timezone
from datetime import timedelta
from .models import CDKey
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from .models import CDKey, User
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user_home')


class UserCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user_home')

def home(request):
    if request.user.is_authenticated:
        # 如果用户已经登录,重定向到用户主页
        return redirect('user_home')
    else:
        # 如果用户未登录,显示主页
        return render(request, 'home.html')

@login_required
def user_home(request):
    # 获取当前登录的用户
    user = request.user

    # 准备渲染模板所需的上下文数据
    context = {
        'user': user,
        # 其他上下文数据...
    }

    # 渲染模板
    return render(request, 'user/home.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('user_home')

def home(request):
    return render(request, 'home.html')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 登录成功后重定向到主页
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_home')
        else:
            error_message = '无效的用户名或密码'
            return render(request, 'user/login.html', {'error_message': error_message})
    else:
        return render(request, 'user/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('user:user_home')

@login_required
def generate_cdkey(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        days = int(request.POST.get('days'))
        amount = int(request.POST.get('amount'))
        
        if request.user.remaining_quota >= amount:
            cdkeys = []
            for _ in range(amount):
                key = generate_unique_cdkey()  # 你需要实现这个函数
                expires_at = timezone.now() + timedelta(days=days)
                cdkey = CDKey.objects.create(key=key, expires_at=expires_at, created_by=request.user)
                cdkeys.append(cdkey)
            
            request.user.remaining_quota -= amount
            request.user.save()
            
            return render(request, 'user/generate_cdkey.html', {'cdkeys': cdkeys})
        else:
            messages.error(request, 'Insufficient quota.')
    
    return render(request, 'user/generate_cdkey.html')

@login_required
def subordinate_list(request):
    subordinates = request.user.subordinates.all()
    return render(request, 'user/subordinate.html', {'subordinates': subordinates})

@login_required
def subordinate_create(request):
    if request.method == 'POST':
        form = SubordinateForm(request.POST)
        if form.is_valid():
            subordinate = form.save(commit=False)
            subordinate.superior = request.user
            subordinate.save()
            return redirect('subordinate_list')
    else:
        form = SubordinateForm()
    return render(request, 'user/subordinate_form.html', {'form': form})

@login_required
def subordinate_edit(request, subordinate_id):
    subordinate = get_object_or_404(User, id=subordinate_id, superior=request.user)
    if request.method == 'POST':
        form = SubordinateForm(request.POST, instance=subordinate)
        if form.is_valid():
            form.save()
            return redirect('subordinate_list')
    else:
        form = SubordinateForm(instance=subordinate)
    return render(request, 'user/subordinate_form.html', {'form': form})

@login_required
def subordinate_delete(request, subordinate_id):
    subordinate = get_object_or_404(User, id=subordinate_id, superior=request.user)
    subordinate.delete()
    return redirect('subordinate_list')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # 重定向到主页或其他页面
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

class UserListView(APIView):
    permission_classes = [IsAdmin | IsAgent]

    def get(self, request):
        if request.user.is_admin():
            users = User.objects.all()
        elif request.user.is_agent1():
            users = request.user.subordinates.all() | User.objects.filter(pk=request.user.pk)
        else:
            users = User.objects.filter(pk=request.user.pk)
        return Response(UserSerializer(users, many=True).data)

@login_required
class UserCreateView(APIView):
    permission_classes = [IsAdmin | IsAgent]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(superior=request.user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
class UserUpdateView(APIView):
    permission_classes = [IsSuperior]

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def cdkey_record(request):
    user = request.user
    records = CDKey.objects.filter(user=user).order_by('-created_at')
    context = {
        'records': records,
    }
    return render(request, 'user/cdkey_record.html', context)

@login_required
def subordinate(request):
    user = request.user
    subordinates = User.objects.filter(superior=user)
    context = {
        'subordinates': subordinates,
    }
    return render(request, 'user/subordinate.html', context)

@login_required
def some_view(request):
    if request.method == 'POST':
        # 处理 POST 请求的逻辑
        # ...
        
        # 处理完成后,重定向到 'user_home' URL
        return redirect(reverse('user_home'))
    else:
        # 处理 GET 请求的逻辑
        # ...
        
        context = {
            'user_home_url': reverse('user_home'),
            # 其他上下文数据...
        }
        
        return render(request, 'user/some_template.html', context)

