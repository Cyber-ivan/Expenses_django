from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Group_users(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @staticmethod
    def create_group(name):
        """
        Создает и возвращает новую группу.

        :param name: Название группы.
        :return: Экземпляр созданной группы.
        :raises ValueError: Если группа с таким именем уже существует.
        """
        if Group_users.objects.filter(name=name).exists():
            raise ValueError("Группа с таким именем уже существует.")

        group = Group_users(name=name)
        group.save()
        return group

    @staticmethod
    def get_group(group_id):
        """
        Возвращает группу по ID.
        """
        return Group_users.objects.get(id=group_id)

    @staticmethod
    def update_group(group_id, name):
        """
        Обновляет название группы.
        """
        group = Group_users.objects.get(id=group_id)
        group.name = name
        group.save()
        return group

    @staticmethod
    def delete_group(group_id):
        """
        Удаляет группу по ID.
        """
        group = Group_users.objects.get(id=group_id)
        group.delete()


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


    @staticmethod
    def get_user(user_id):
        """
        Возвращает пользователя по ID.
        """
        return User.objects.get(id=user_id)


    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @staticmethod
    def create_category(name):
        """
        Создает и возвращает новую категорию.
        """
        if Category.objects.filter(name=name).exists():
            raise ValueError("Категория с таким именем уже существует.")

        category = Category(name=name)
        category.save()
        return category

    @staticmethod
    def get_category(category_id):
        """
        Возвращает категорию по ID.
        """
        return Category.objects.get(id=category_id)

    @staticmethod
    def update_category(category_id, name):
        """
        Обновляет название категории.
        """
        category = Category.objects.get(id=category_id)
        category.name = name
        category.save()
        return category

    @staticmethod
    def delete_category(category_id):
        """
        Удаляет категорию по ID.
        """
        category = Category.objects.get(id=category_id)
        category.delete()


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    money = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(null=True, blank=True)
    income = models.BooleanField(default=False)  # True: доход, False: расход
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_expense(user, money, category=None, comment=None, income=False):
        """
        Создает и возвращает новую запись о расходе/доходе.
        """
        expense = Expense(
            user=user,
            category=category,
            money=money,
            comment=comment,
            income=income,
        )
        expense.save()
        return expense

    @staticmethod
    def get_expense(expense_id):
        """
        Возвращает запись о расходе/доходе по ID.
        """
        return Expense.objects.get(id=expense_id)

    @staticmethod
    def update_expense(expense_id, **kwargs):
        """
        Обновляет данные о расходе/доходе.
        """
        expense = Expense.objects.get(id=expense_id)
        for key, value in kwargs.items():
            setattr(expense, key, value)
        expense.save()
        return expense

    @staticmethod
    def delete_expense(expense_id):
        """
        Удаляет запись о расходе/доходе по ID.
        """
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
