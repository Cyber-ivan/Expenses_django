from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Expense, Category, Group_users
from django.shortcuts import get_object_or_404
from expense.forms import UserCreationForm
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse


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

        if 'update_name' in request.POST:
            request.user.first_name = request.POST.get('first_name', '').strip()
            request.user.save()

        elif 'update_surname' in request.POST:
            request.user.last_name = request.POST.get('last_name', '').strip()
            request.user.save()

        elif 'update_balance' in request.POST:
            balance = request.POST.get('balance')
            if balance and balance.replace('.', '', 1).isdigit():
                request.user.money = float(balance)
                request.user.save()

        elif 'create_group' in request.POST:
            group_name = request.POST.get('group_name', '').strip()
            if group_name:
                new_group, created = Group_users.objects.get_or_create(name=group_name)
                if created:  # Если группа создана впервые, связываем с пользователем
                    request.user.my_groups.add(new_group)

        return HttpResponseRedirect(reverse('settings'))


class Home(View):
    template_name = 'home.html'

    @method_decorator(login_required)
    def get(self, request):
        categories = Category.objects.all()
        expenses = Expense.objects.filter(user=request.user).order_by('-date')

        context = {
            'categories': categories,
            'expenses': expenses,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        money = request.POST.get('money')
        category_id = request.POST.get('category_in')
        comment = request.POST.get('comment')
        income = True if request.POST.get('income') else False

        # Создаём новый расход
        expense = Expense.objects.create(
            user=request.user,
            money=money,
            category_id=category_id,
            comment=comment,
            income=income
        )
        # categories = Category.objects.all()
        # expenses = Expense.objects.filter(user=request.user)
        # incomes = Expense.objects.filter(user=request.user, income=True)
        #
        # context = {
        #     'categories': categories,
        #     'expenses': expenses,
        #     'incomes': incomes,
        # }

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
