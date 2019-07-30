from django.db import models
from django.contrib.auth.models import AbstractUser

"""django内置提供了User模型，它包含了：
        username，即用户名
        password，密码
        email，邮箱
        first_name，名
        last_name，姓
    以上字段，我们可以通过继承它的父类AbstractUser进行对User的扩展
    注意一定要继承 AbstractUser，而不是继承 auth.User。尽管 auth.User 继承自 AbstractUser 且并没有对其进行任何额外拓展,
    但 AbstractUser 是一个抽象类，而 auth.User 不是。如果你继承了 auth.User 类，这会变成多表继承，
    在目前的情况下这种继承方式是不被推荐的。
"""


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass