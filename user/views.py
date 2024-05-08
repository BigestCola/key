# user/views.py

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
from datetime import timedelta
from .models import CDKey
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from .models import CDKey, User
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Profile
from django.contrib import messages
from .models import CDKey, Profile
import uuid
from .models import User, CDKey
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from user.models import CDKey
from datetime import datetime
from django.db.models import Q
from django.db.models import Count, Q, F, ExpressionWrapper, fields
from datetime import timedelta
from datetime import timedelta, date
from django.db.models import Sum


@login_required
def subordinate_cdkey_record(request, subordinate_id):
    subordinate = get_object_or_404(User, id=subordinate_id, superior=request.user)
    
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        
        query = Q(created_by=subordinate)
        
        if month and year:
            query &= Q(created_at__year=year, created_at__month=month)
        elif year:
            query &= Q(created_at__year=year)
        
        records = CDKey.objects.filter(query).order_by('-created_at')
    else:
        records = CDKey.objects.filter(created_by=subordinate).order_by('-created_at')
    
    current_year = date.today().year
    years = range(current_year, current_year - 10, -1)
    
    records = records.annotate(
        remaining_days=ExpressionWrapper(
            F('expires_at') - date.today(),
            output_field=fields.DurationField()
        )
    )
    
    validity_days_distribution = records.values('validity_days').annotate(count=Count('id')).order_by('validity_days')
    
    # 将有效期天数转换为天数,并按天数分组
    validity_days_distribution = {
        distribution['validity_days']: distribution['count']
        for distribution in validity_days_distribution
    }
    
    summary = {
        'total': records.count(),
        'validity_days_distribution': validity_days_distribution,
    }
    
    context = {
        'subordinate': subordinate,
        'records': records,
        'current_year': current_year,
        'years': years,
        'summary': summary,
    }
    return render(request, 'user/subordinate_cdkey_record.html', context)




def cdkey_monthly_summary(request):
    # 获取当前用户的本月 CDKey 记录
    current_month = datetime.now().month
    current_year = datetime.now().year
    cdkeys = CDKey.objects.filter(created_by=request.user, created_at__month=current_month, created_at__year=current_year)
    
    # 计算汇总数据
    total_cdkeys = cdkeys.count()
    total_days = sum(cdkey.validity_days for cdkey in cdkeys)
    
    context = {
        'cdkeys': cdkeys,
        'total_cdkeys': total_cdkeys,
        'total_days': total_days,
    }
    return render(request, 'user/cdkey_monthly_summary.html', context)

def cdkey_custom_summary(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # 检查日期是否为空
        if not start_date or not end_date:
            # 处理空日期的情况,例如设置默认值或返回错误信息
            start_date = '2000-01-01'  # 设置默认的开始日期
            end_date = datetime.now().strftime('%Y-%m-%d')  # 设置默认的结束日期为当前日期
        
        # 将日期字符串转换为日期时间对象
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # 获取指定时间段内的 CDKey 记录
        cdkeys = CDKey.objects.filter(created_by=request.user, created_at__range=[start_date, end_date])
        
        # 计算汇总数据
        total_cdkeys = cdkeys.count()
        total_days = sum(cdkey.validity_days for cdkey in cdkeys)
        
        context = {
            'cdkeys': cdkeys,
            'total_cdkeys': total_cdkeys,
            'total_days': total_days,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, 'user/cdkey_custom_summary.html', context)
    else:
        return render(request, 'user/cdkey_custom_summary.html')

def subordinate_cdkeys_monthly_summary(request, user_id):
    subordinate = get_object_or_404(User, id=user_id)
    if not can_manage_user(request.user, subordinate):
        return HttpResponseForbidden("You don't have permission to view this user's CDKeys.")

    now = timezone.now()
    one_month_ago = now - timedelta(days=30)
    cdkeys = CDKey.objects.filter(created_by=subordinate, created_at__gte=one_month_ago)
    summary = cdkeys.values('validity_days').annotate(count=Count('validity_days'))

    context = {
        'subordinate': subordinate,
        'summary': summary,
    }
    return render(request, 'user/subordinate_cdkeys_monthly_summary.html', context)

def subordinate_cdkeys_custom_summary(request, user_id):
    subordinate = get_object_or_404(User, id=user_id)
    if not can_manage_user(request.user, subordinate):
        return HttpResponseForbidden("You don't have permission to view this user's CDKeys.")

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    cdkeys = CDKey.objects.filter(created_by=subordinate, created_at__range=[start_date, end_date])
    summary = cdkeys.values('validity_days').annotate(count=Count('validity_days'))

    context = {
        'subordinate': subordinate,
        'summary': summary,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'user/subordinate_cdkeys_custom_summary.html', context)

def can_manage_user(superior, subordinate):
    if superior.is_superuser:
        return True
    elif superior.role == User.ROLE_ADMIN:
        return True
    elif superior.role == User.ROLE_FIRST_LEVEL_AGENT and subordinate.superior == superior:
        return True
    else:
        return False

def subordinate_cdkeys_view(request, user_id):
    subordinate = get_object_or_404(User, id=user_id)
    if not can_manage_user(request.user, subordinate):
        return HttpResponseForbidden("You don't have permission to view this user's CDKeys.")

    cdkeys = CDKey.objects.filter(created_by=subordinate)
    context = {
        'subordinate': subordinate,
        'cdkeys': cdkeys,
    }
    return render(request, 'user/subordinate_cdkeys.html', context)

def dashboard_view(request):
    if request.user.is_authenticated:
        user = request.user
        if is_admin(user):
            subordinates = User.objects.exclude(id=user.id)
        elif is_first_level_agent(user):
            subordinates = User.objects.filter(superior=user)
        else:
            subordinates = []

        cdkey_info = []
        for subordinate in subordinates:
            cdkeys = CDKey.objects.filter(created_by=subordinate)
            cdkey_info.append({
                'subordinate': subordinate,
                'cdkeys': cdkeys
            })

        context = {
            'user': user,
            'subordinates': subordinates,
            'cdkey_info': cdkey_info
        }
        return render(request, 'user/dashboard.html', context)
    else:
        return redirect('user:login')

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
        return redirect('user:user_home')
    else:
        # 如果用户未登录,显示主页
        return render(request, 'user/home.html')



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
    return redirect('user:user_home')

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:home')  # 登录成功后重定向到主页
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
            return redirect('user:home')
        else:
            error_message = '无效的用户名或密码'
            return render(request, 'user/login.html', {'error_message': error_message})
    else:
        return render(request, 'user/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('user:user_home')

def generate_unique_cdkey():
    return str(uuid.uuid4())

@login_required
def generate_cdkey(request):
    user = request.user
    
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    if request.method == 'POST':
        days = int(request.POST.get('days'))
        amount = int(request.POST.get('amount'))
        
        if profile.remaining_quota >= amount:
            cdkeys = []
            for _ in range(amount):
                key = generate_unique_cdkey()
                expires_at = timezone.now() + timedelta(days=days)
                cdkey = CDKey.objects.create(key=key, expires_at=expires_at, created_by=user, validity_days=days)
                cdkeys.append(cdkey)
            
            profile.remaining_quota -= amount
            profile.save()
            
            return render(request, 'user/generate_cdkey.html', {'cdkeys': cdkeys, 'success': True})
        else:
            messages.error(request, '配额不足，请联系上级')
    
    return render(request, 'user/generate_cdkey.html')

@login_required
def subordinate_list(request):
    subordinates = request.user.subordinates.all()
    
    admin_profile = request.user.profile
    total_credit = admin_profile.credit if admin_profile.credit else 0
    remaining_credit = admin_profile.remaining_quota if admin_profile.remaining_quota else 0
    
    context = {
        'subordinates': subordinates,
        'total_credit': total_credit,
        'remaining_credit': remaining_credit,
    }
    
    return render(request, 'user/subordinate.html', context)



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
                return redirect('user:user_home') # 重定向到主页或其他页面
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


@login_required
def cdkey_record(request):
    user = request.user
    
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        subordinate_id = request.POST.get('subordinate')
        
        # 构建查询条件
        query = Q()
        if subordinate_id:
            subordinate = User.objects.get(id=subordinate_id)
            query &= Q(created_by=subordinate)
        else:
            # 如果没有选择下级用户,则根据当前用户的角色查询记录
            if user.is_superuser or user.is_staff:
                # 如果是上级用户,则查询自己和所有下级用户的记录
                subordinates = User.objects.filter(superior=user)
                query &= Q(created_by__in=[user] + list(subordinates))
            else:
                # 如果是普通用户,则只查询自己的记录
                query &= Q(created_by=user)
        
        if month and year:
            query &= Q(created_at__year=year, created_at__month=month)
        elif year:
            query &= Q(created_at__year=year)
        
        records = CDKey.objects.select_related('created_by').filter(query).order_by('-created_at')
    else:
        # 如果不是POST请求,则根据当前用户的角色查询记录
        if user.is_superuser or user.is_staff:
            # 如果是上级用户,则查询自己和所有下级用户的记录
            subordinates = User.objects.filter(superior=user)
            records = CDKey.objects.select_related('created_by').filter(created_by__in=[user] + list(subordinates)).order_by('-created_at')
        else:
            # 如果是普通用户,则只查询自己的记录
            records = CDKey.objects.select_related('created_by').filter(created_by=user).order_by('-created_at')
    
    # 获取当前年份和所有可选年份
    current_year = datetime.now().year
    years = range(current_year, current_year - 10, -1)
    
    # 获取下级用户列表
    subordinates = []
    if user.is_superuser or user.is_staff:
        subordinates = User.objects.filter(superior=user)
    
    context = {
        'records': records,
        'current_year': current_year,
        'years': years,
        'subordinates': subordinates,
    }
    return render(request, 'user/cdkey_record.html', context)


@login_required
def some_view(request):
    if request.method == 'POST':
        # 处理 POST 请求的逻辑
        # ...
        
        # 处理完成后,重定向到 'home' URL
        return redirect(reverse('user:home'))
    else:
        # 处理 GET 请求的逻辑
        # ...
        
        context = {
            'user_home_url': reverse('user:home'),
            # 其他上下文数据...
        }
        
        return render(request, 'user/some_template.html', context)


