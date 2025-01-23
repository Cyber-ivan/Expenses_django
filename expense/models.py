from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Group_users(models.Model):
    name = models.CharField(max_length=255, unique=True)


class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    telegram_id = models.BigIntegerField(null=True, blank=True)
    money = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    my_groups = models.ManyToManyField(Group_users)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    money = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(null=True, blank=True)
    income = models.BooleanField(default=False)  # True: доход, False: расход
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.money} {self.category.name}"

