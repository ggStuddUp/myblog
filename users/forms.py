"""关于表单的代码一般在在这里"""

# django内置的用户注册表单：
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 自定义用户注册表单
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # 指定注册的用户模型为自定义的User模型
        fields = ("username", "email")  # 指定注册表单渲染的控件，密码和确认密码在UserCreationForm中已定义