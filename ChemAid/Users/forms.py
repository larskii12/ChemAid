# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import User
from django.contrib.auth import (
    authenticate,
    get_user_model

)

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'student_number', 'contact_no', 'course', 'year_lvl', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'student_number', 'contact_no', 'course', 'year_lvl', 'password1', 'password2']

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'student_number', 'contact_no', 'course', 'year_lvl', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField( required = False)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False )
    contact_no = forms.CharField(required = False )
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'contact_no', 'course']

  

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm,self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['first_name'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['last_name'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['contact_no'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['course'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['course'].required=False
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
      
        )

class ProfileUpdateForm(forms.ModelForm):
    image= forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['image']

class adminupdateform(forms.ModelForm):
    #email = forms.EmailField( required = False)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False )
    contact_no = forms.CharField(required = False )
    class Meta:
        model = User
        fields = ['first_name','last_name', 'contact_no']

    def __init__(self, *args, **kwargs):
        super(adminupdateform,self).__init__(*args, **kwargs)
        #self.fields['email'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['first_name'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['last_name'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['contact_no'].widget.attrs['style'] = 'width:350px; height:40px;'
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
      
        )

class AdminDetailsForm(forms.Form):
    
    class Meta:
        model = User
        fields = ['first_name','last_name','contact_no']

    def __init__(self, *args, **kwargs):
        super(AdminDetailsForm,self).__init__(*args, **kwargs)
        #self.fields['email'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['first_name'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['last_name'].widget.attrs['style'] = 'width:350px; height:40px;'
        self.fields['contact_no'].widget.attrs['style'] = 'width:350px; height:40px;'
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-4 mb-0'),
                Column('last_name', css_class='form-group col-md-4 mb-0'),
                Column('contact_no', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
      
        )
