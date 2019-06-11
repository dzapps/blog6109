from django import forms

from django.contrib.auth import (
    authenticate,
    get_user_model,

)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='帳號')
    password = forms.CharField(widget=forms.PasswordInput, label='密碼')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('使用者不存在')
            if not user.check_password(password):
                raise forms.ValidationError('密碼錯誤')

        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='密碼')
    password2 = forms.CharField(widget=forms.PasswordInput, label='密碼確認')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError('信箱已被註冊!')

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError('密碼不一致!')

        return password