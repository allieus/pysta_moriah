# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.core.validators import EmailValidator


# 회원 가입 form
class RegistrationForm(UserCreationForm):
    email = forms.CharField(validators=[EmailValidator()])
    profile_photo = forms.FileField(required=False)
    
    # 이메일 중복 체크
    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        if email:
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError('이미 등록된 이메일입니다.')
        return email

    # 저장
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        
        if commit:
            user.save()
            
        return user

# 회원 수정 form
class ModificationForm(forms.ModelForm):
    profile_photo = forms.FileField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = get_user_model()
        fields = ('email', )

    # password 체크
    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        
        # 패스워드를 변경하는 경우에만 체크
        if not password: return
        if password != password2:
            raise forms.ValidationError(u"패스워드가 일치하지 않습니다")
        
    # email 체크
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            if self.instance.email != email and get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError('이미 등록된 이메일입니다.')
        return email
    
    # 저장
    def save(self, commit=True):
        user = super(ModificationForm, self).save(commit)
        password = self.cleaned_data.get('password', '')

        if password:
            user.set_password(password)

        return user


# 로그인 form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)

            # 로그인 fail
            if self.user is None:
                # 로그인 실패 이유를 찾기 위해서 사용자 검색
                if get_user_model().objects.filter(username=username).exists():
                    raise forms.ValidationError(u"패스워드 오류")
                else:
                    raise forms.ValidationError(u"계정 오류")
            
            # 이메일 인증 fail
            if not self.user.is_active:
                raise forms.ValidationError(u"인증되지 않은 사용자 입니다")

# 인증키 재발송 form
class ActivationForm(forms.Form):
    email = forms.CharField(validators=[EmailValidator()])

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            users = get_user_model().objects.filter(email=email)
            if users.count() == 0:
                raise forms.ValidationError('등록되지 않은 이메일입니다.')
            else:
                self.user = users[0]

        return email
