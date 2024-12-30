from django import forms
from .models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=65, widget=forms.PasswordInput, label="Введіть пароль")
    confirm_password = forms.CharField(max_length=65, widget=forms.PasswordInput, label="Підтвердіть пароль")

    class Meta:
        model = User
        fields = ['email',]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Паролі не співпадають👍')
        return cleaned_data


    def save(self, commit = True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)

        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=128,label="Введiть email")
    password = forms.CharField(max_length=65, widget=forms.PasswordInput, label="Введіть пароль")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = authenticate(email=email,password=password)
        if user is None:
            raise ValidationError("Данні не співпадають")

        self.user = user
        return cleaned_data
    # def get_user(self):
    #     return getattr(self,"user",None)


