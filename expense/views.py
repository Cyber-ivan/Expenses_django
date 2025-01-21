from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect

from expense.forms import UserCreationForm


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
            user = form.save()  # Сохраняем пользователя
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Аутентифицируем пользователя
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Логиним пользователя
                return redirect('home')

            # Если аутентификация не удалась, возвращаем ошибку
            form.add_error(None, "Authentication failed. Please try again.")

        # Если форма невалидна, возвращаем её с ошибками
        context = {
            'form': form
        }
        return render(request, self.template_name, context)