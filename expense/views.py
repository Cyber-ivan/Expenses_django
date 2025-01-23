from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import Expense, Category, Group_users, User
from expense.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.views import View


class Settings(View):
    template_name = 'settings.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        groups = Group_users.objects.filter(user=request.user)
        context = {
            'user': request.user,
            'groups': groups,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Обработка POST-запросов для обновления данных пользователя и работы с группами."""
        if 'update_name' in request.POST:
            self.update_name(request)

        elif 'update_surname' in request.POST:
            self.update_surname(request)

        elif 'update_balance' in request.POST:
            self.update_balance(request)

        elif 'create_group' in request.POST:
            self.create_group(request)

        elif 'add_member' in request.POST:
            self.add_member_to_group(request)

        return HttpResponseRedirect(reverse('settings'))

    def update_name(self, request):
        """Обновление имени пользователя."""
        first_name = request.POST.get('first_name', '').strip()
        if first_name:
            request.user.first_name = first_name
            request.user.save()

    def update_surname(self, request):
        """Обновление фамилии пользователя."""
        last_name = request.POST.get('last_name', '').strip()
        if last_name:
            request.user.last_name = last_name
            request.user.save()

    def update_balance(self, request):
        """Обновление текущего баланса пользователя."""
        balance = request.POST.get('balance', '').strip()
        if balance and balance.replace('.', '', 1).isdigit():
            request.user.money = float(balance)
            request.user.save()

    def create_group(self, request):
        """Создание новой группы."""
        group_name = request.POST.get('group_name', '').strip()
        if group_name:
            with transaction.atomic():
                new_group, created = Group_users.objects.get_or_create(name=group_name)
                if created:
                    # Привязываем созданную группу к пользователю
                    request.user.my_groups.add(new_group)

    def add_member_to_group(self, request):
        """Добавление участника в группу."""
        group_id = request.POST.get('group_id')
        email = request.POST.get('email', '').strip()
        if group_id and email:
            group = get_object_or_404(Group_users, id=group_id)
            member = get_object_or_404(User, email=email)
            if request.user.my_groups.filter(id=group.id).exists():
                member.my_groups.add(group)


class Home(View):
    template_name = 'home.html'

    @method_decorator(login_required)
    def get(self, request):
        # Личные расходы
        personal_expenses = Expense.objects.filter(user=request.user).order_by('-date')

        # Группы пользователя
        user_groups = request.user.my_groups.all()

        # Расходы всех групп, где состоит пользователь
        group_expenses = []
        for group in user_groups:
            group_expenses += Expense.objects.filter(user__my_groups=group).order_by('-date')

        context = {
            'personal_expenses': personal_expenses,
            'user_groups': user_groups,
            'group_expenses': group_expenses,
            'categories': Category.objects.all(),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        money = request.POST.get('money')
        category_id = request.POST.get('category_in')
        comment = request.POST.get('comment')
        income = True if request.POST.get('income') else False

        # Проверяем, добавляется ли личный или групповой расход
        group_id = request.POST.get('group_id')  # ID выбранной группы
        if group_id:
            group = Group_users.objects.get(id=group_id)
            expense = Expense.objects.create(
                user=request.user,
                money=money,
                category_id=category_id,
                comment=comment,
                income=income
            )
        else:
            expense = Expense.objects.create(
                user=request.user,
                money=money,
                category_id=category_id,
                comment=comment,
                income=income
            )

        return HttpResponseRedirect(reverse('home'))


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')

        # Если форма невалидна, возвращаем её с ошибками
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
