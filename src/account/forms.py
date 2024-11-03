from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    
    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")
        
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ('email', 'password')
        
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")
            
class AccountUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ('email', 'username')
        
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % account)
    
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % account)
    
    

User = get_user_model()

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)  # Cherche l'utilisateur par email
            except User.DoesNotExist:
                raise forms.ValidationError("Email or password is incorrect.")

            # Vérifiez que le mot de passe est correct
            if not user.check_password(password):
                raise forms.ValidationError("Email or password is incorrect.")
            self.cleaned_data['user'] = user  # Ajoutez l'utilisateur aux données nettoyées
        return self.cleaned_data