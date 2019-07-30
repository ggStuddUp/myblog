from django.shortcuts import render, redirect
from .forms import RegisterForm  # 导入注册表单模型


def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = None
    if request.method == 'GET':
        redirect_to = request.GET.get('next', '')
    # 判断提交方式是否为POST,是POST方式说明用户已经提交注册信息
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # 通过POST提价的参数生成注册表单
        redirect_to = request.POST.get('next')

        # 验证数据的合法性
        if form.is_valid():
            form.save()  # 合法则保存
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    # 不是POST方式说明用户正访问注册页面
    else:
        form = RegisterForm()  # 提交方式不是POST，返回空的注册表单
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})