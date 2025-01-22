from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Expense, Category
User = get_user_model()


class HomePage(forms.Form):
    category = forms.CharField(required=False, label="Category", max_length=100)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['money', 'category', 'comment', 'income']

    # Пример для выбора категории, если категории пустые, выберем "No category"
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")