from django import forms

class AdminProfileForm(forms.Form):
    name = forms.CharField(label="ПІБ", max_length=100, required=False)
    email = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Новий пароль", widget=forms.PasswordInput, required=False)
