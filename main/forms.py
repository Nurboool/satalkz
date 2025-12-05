# main/forms.py – ТОЛЫҚ ТҮЗЕТІЛГЕН НҰСҚА
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Ad


# ТІРКЕЛУ ФОРМАСЫ
class RegisterForm(UserCreationForm):
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 777 123 4567'
        })
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'phone', 'password1', 'password2', 'role')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Қолданушы аты'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Құпия сөз өрістеріне стиль қосу
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Құпия сөз'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Құпия сөзді қайталау'
        })


# ЖАРНАМА ФОРМАСЫ
class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category', 'city']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'iPhone 14 Pro 256GB',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Жақсы жағдайда...',
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': '1 500 000',
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Тақырып',
            'description': 'Сипаттама',
            'price': 'Бағасы (тг)',
            'category': 'Категория',
            'city': 'Қала',
        }