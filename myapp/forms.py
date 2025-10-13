from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class AppLogin(AuthenticationForm):
    username = UsernameField(label='Nombre de Usuario', widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class':'form-control'}), required=False)

    class Meta:
        fields = ('username', 'password')
    
    #def confirm_login_allowed(self, user):
    #    if user.is_staff and not user.is_superuser:
    #        raise ValidationError(("This account is not allowed here."),code='not_allowed',)
