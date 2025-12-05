# main/urls.py ← ТОЛЫҒЫМЕН ОСЫЛАЙ БОЛСЫН!
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.headd, name='headd'),

    # Сенің ескі тапсырмаларың (өзгертпей қалдырдым)
    path('pract1/', views.index, name='index'),
    path('pract2/', views.shop, name='shop'),
    path('exchange/', views.exchange, name='exchange'),
    path('history/', views.history_view, name='history'),
    path('combo/', views.combo_ac, name='combo_ac'),
    path('pars/', views.pars, name='pars'),
    path('Pars_valute/', views.pars, name='pars_valute'),
    path('lab5.1/', views.tempp, name='tempp'),
    path('lab5.2/', views.planshety_parser_view, name='export'),
    path('lab6/', views.aud6, name='aud6'),
    path('aud7/', views.aud7, name='aud7'),
    path('aud7/result/', views.aud7_result, name='aud7_result'),
    path('aud7/tapsyrma/', views.aud7_tapsyrma, name='aud7_tapsyrma'),

    # Авторизация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='main/auth/login.html',
        next_page='/olx/'
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Профиль
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/password/', auth_views.PasswordChangeView.as_view(
        template_name='main/auth/password_change.html',
        success_url='/profile/'
    ), name='password_change'),

    path('change-password/', views.change_password, name='change_password'),
    path('analytics/', views.analytics, name='analytics'),

    # OLX жүйесі
    path('olx/', views.all_ads, name='all_ads'),
    path('olx/ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('olx/create/', views.create_ad, name='create_ad'),
    path('olx/my/', views.my_ads, name='my_ads'),
    path('olx/moderate/', views.moderate_ads, name='moderate_ads'),
    path('olx/ad/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('olx/ad/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),

    path('manage-users/', views.manage_users, name='manage_users'),
    path('change-role/<int:user_id>/', views.change_user_role, name='change_user_role'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    # Құпия сөзді қалпына келтіру
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='main/auth/password_reset.html',
        email_template_name='main/auth/password_reset_email.html',
        subject_template_name='main/auth/password_reset_subject.txt',
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='main/auth/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='main/auth/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='main/auth/password_reset_complete.html'
    ), name='password_reset_complete'),
]