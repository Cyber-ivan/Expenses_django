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


class Test(View):
    template_name = 'test.html'

    def get(self, request):
        categories = Category.objects.all()  # Загрузка всех категорий

        context = {
            'categories': categories,
        }
        return render(request, self.template_name, context)
class Home(View):
    template_name = 'expense/home.html'

    @method_decorator(login_required)
    def get(self, request):
        expenses = Expense.objects.filter(user=request.user, income=False)
        incomes = Expense.objects.filter(user=request.user, income=True)
        categories = Category.objects.all()  # Загрузка всех категорий

        context = {
            'user': request.user.username,
            'expenses': expenses,
            'incomes': incomes,
            'categories': categories,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        category_id = request.POST.get('category')
        money = request.POST.get('money')
        comment = request.POST.get('comment')
        income = request.POST.get('income', False) == 'on'

        if not money:
            return self.get(request)  # Перезагрузка с формой ошибки

        category = get_object_or_404(Category, id=category_id) if category_id else None
        Expense.objects.create(
            user=request.user,
            category=category,
            money=money,
            comment=comment,
            income=income
        )
        return self.get(request)  # Перезагрузка после добавления


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
