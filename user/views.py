# user/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from .permissions import IsAdmin, IsAgent, IsSuperior
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import SubordinateForm

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

class UserCreateView(APIView):
    permission_classes = [IsAdmin | IsAgent]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(superior=request.user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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