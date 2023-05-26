from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import NewUser

INPUTSTYLE = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
USERNAME_REGEX = ['%','$','&','*','#']

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = NewUser
        fields = ('email', 'username', 'first_name', 'country','last_name', 'gender', 'phone_number' ,'id_image')

    def clean_password2(self, contain=False):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        if len(password1) < 8:
            raise ValidationError("Passwords Must be More 8 Charcaters")

        for char in USERNAME_REGEX:
            if char in password1:
                contain = True

        if not contain:
            raise ValidationError("Passwords Must Contain one of '% - $ - & - * - #'")
        return password2

    # def clean_first_name(self):
    #     firstname = self.cleaned_data.get('first_name')
    #     if len(firstname)<6:
    #         raise ValidationError("Fist name must be More 6 Charcaters")
    #     return firstname

    # def clean_last_name(self):
    #     lastname = self.cleaned_data.get('last_name')
    #     if len(lastname)<6:
    #         raise ValidationError("Last name must be More 6 Charcaters")
    #     return lastname
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username)<6:
            raise ValidationError("User name must be More 6 Charcaters")
        return username

    # def clean_length(self):
    #     firstname = self.cleaned_data.get('firstname')
    #     lastname = self.cleaned_data.get('lastname')
    #     username = self.cleaned_data.get('username')
    #     if len(lastname)<5:
    #         raise ValidationError("Last name must be More 5 Charcaters")
    #     if len(username)<5:
    #         raise ValidationError("User name must be More 5 Charcaters")
    #     return firstname, lastname, username



        return firstname

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = INPUTSTYLE

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = NewUser
        fields = ('email', 'password', 'date_of_birth',
                  'is_active', 'is_admin')


class RegisterForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = ('email', 'username', 'first_name', 'last_name')