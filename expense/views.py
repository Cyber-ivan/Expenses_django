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
        if 'update' in request.POST:
            self.update(request)

        elif 'create_group' in request.POST:
            self.create_group(request)

        elif 'add_member' in request.POST:
            self.add_member_to_group(request)

        return HttpResponseRedirect(reverse('settings'))

    def update(self, request):
        """Обновление имени пользователя."""
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        money = request.POST.get('balance', '').strip()
        try:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.money = float(money)
            request.user.save()
        except Exception as e:
            print(e)

    def create_group(self, request):
        """Создание новой группы."""
        group_name = request.POST.get('group_name', '').strip()
        if group_name:
            with transaction.atomic():
                new_group, created = Group_users.objects.get_or_create(name=group_name)
                if created:
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
        personal_expenses = Expense.objects.filter(user=request.user).order_by('-date')
        user_groups = request.user.my_groups.all()
        selected_group_id = request.GET.get('group_id') or (user_groups.first().id if user_groups.exists() else None)
        participants = []
        group_expenses = []

        if selected_group_id:
            group = Group_users.objects.get(id=selected_group_id)
            participants = group.user_set.all()
            group_expenses = Expense.objects.filter(user__my_groups=group).order_by('-date')

        selected_participants = request.GET.getlist('participants')
        if selected_participants:
            group_expenses = group_expenses.filter(user_id__in=selected_participants)

        context = {
            'personal_expenses': personal_expenses,
            'user_groups': user_groups,
            'group_expenses': group_expenses,
            'categories': Category.objects.all(),
            'selected_group_id': selected_group_id,
            'participants': participants,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        money = request.POST.get('money')
        category_id = request.POST.get('category_in')
        comment = request.POST.get('comment')
        income = True if request.POST.get('income') else False
        group_id = request.POST.get('group_id')
        selected_participants = request.POST.getlist('participants')

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
