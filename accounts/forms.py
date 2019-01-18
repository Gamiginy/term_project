from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        if User.USERNAME_FIELD == 'email':
            fields = ('email',
                      'email',
                      'first_name',
                      'last_name',
                      'school_year',
                      'school_grade',
                      'department',
                      'secret_question',
                      'secret_question_answer'
            )
        else:
            fields = (
                'username',
                'email',
                'first_name',
                'last_name',
                'school_year',
                'school_year',
                'school_grade',
                'department',
                'secret_question',
                'secret_question_answer'
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
