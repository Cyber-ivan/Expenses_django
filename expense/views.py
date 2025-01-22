from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Expense, Category
from django.shortcuts import get_object_or_404
from expense.forms import UserCreationForm
from django.shortcuts import render
from django.views import View
from .forms import HomePage
from .forms import ExpenseForm
from django.http import HttpResponseRedirect
from django.urls import reverse

class Home(View):
    template_name = 'home.html'

    @method_decorator(login_required)
    def get(self, request):
        categories = Category.objects.all()
        expenses = Expense.objects.filter(user=request.user)
        incomes = Expense.objects.filter(user=request.user, income=True)

        context = {
            'categories': categories,
            'expenses': expenses,
            'incomes': incomes,
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
        categories = Category.objects.all()
        expenses = Expense.objects.filter(user=request.user)
        incomes = Expense.objects.filter(user=request.user, income=True)

        context = {
            'categories': categories,
            'expenses': expenses,
            'incomes': incomes,
        }

        return HttpResponseRedirect(reverse('test'))


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
