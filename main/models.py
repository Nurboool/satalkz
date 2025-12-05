# main/models.py - ТОЛЫҚ ДҰРЫС НҰСҚА
from django.contrib.auth.models import AbstractUser
from django.db import models


# БІРІНШІ - User моделі
class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Қолданушы'),
        ('director', 'Компания директоры'),
        ('admin', 'Әкімші'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name="Рөл")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Компания аты")
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name="Мекен-жай")
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Қала")

    def is_director(self):
        return self.role == 'director'

    def is_admin_user(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# ЕКІНШІ - Category, City, Ad, AdImage
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категориялар"


class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Қала")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Қала"
        verbose_name_plural = "Қалалар"


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField(max_length=200, verbose_name="Тақырып")
    description = models.TextField(verbose_name="Сипаттама")
    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="Бағасы")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Қала")
    is_moderated = models.BooleanField(default=False, verbose_name="Модерациядан өтті")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Жарияланды")
    views = models.PositiveIntegerField(default=0, verbose_name="Көрулер")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Жарнама"
        verbose_name_plural = "Жарнамалар"
        ordering = ['-created_at']


class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images', verbose_name="Жарнама")
    image = models.ImageField(upload_to='ads/', verbose_name="Сурет")

    def __str__(self):
        return f"{self.ad.title} - сурет"

    class Meta:
        verbose_name = "Жарнама суреті"
        verbose_name_plural = "Жарнама суреттері"