from django import forms
from django.contrib.auth.models import User
from .models import Student, Application, Documents, Course, ContactMessage
class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'dob', 'gender', 'address', 'city', 'state', 'pincode']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Complete Mailing Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
        }
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['course']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
        }
class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-md py-3 bg-surface-container border-2 border-transparent focus:border-primary focus:bg-white rounded-lg transition-all outline-none text-body-sm font-body-sm',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-md py-3 bg-surface-container border-2 border-transparent focus:border-primary focus:bg-white rounded-lg transition-all outline-none text-body-sm font-body-sm',
                'placeholder': 'Your Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-md py-3 bg-surface-container border-2 border-transparent focus:border-primary focus:bg-white rounded-lg transition-all outline-none text-body-sm font-body-sm',
                'placeholder': 'Your Phone Number (Optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-md py-3 bg-surface-container border-2 border-transparent focus:border-primary focus:bg-white rounded-lg transition-all outline-none text-body-sm font-body-sm',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-md py-3 bg-surface-container border-2 border-transparent focus:border-primary focus:bg-white rounded-lg transition-all outline-none text-body-sm font-body-sm',
                'rows': 5,
                'placeholder': 'How can we help you? Please describe your query...'
            }),
        }

