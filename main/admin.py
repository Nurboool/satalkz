# main/admin.py – ТОЛЫҚ ДҰРЫС НҰСҚА
from django.contrib import admin
from .models import User, Category, City, Ad, AdImage

# User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'phone')

# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# City
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Ad
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'city', 'is_moderated', 'created_at')
    list_filter = ('is_moderated', 'category', 'city')
    search_fields = ('title', 'description')

# AdImage
@admin.register(AdImage)
class AdImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad', 'image')