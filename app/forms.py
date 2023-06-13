from django import forms


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=50)
    last_name = forms.CharField(label='Фамилия', max_length=50)
    email = forms.EmailField(label='Почта', max_length=50)
    username = forms.CharField(label='Логин', max_length=50)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, max_length=50)
    repeated_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, max_length=50)


class EditProfileForm(forms.Form):
    username = forms.CharField(label='Логин', required=False)
    email = forms.CharField(label='Почта', required=False)
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)


class AnswerForm(forms.Form):
    text = forms.CharField(label='Новый комментарий', max_length=100, widget=forms.Textarea(attrs={'rows': '3'}))