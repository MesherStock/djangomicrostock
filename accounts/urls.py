from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgotpassword/', views.forgotPassword, name='forgotPassword'),
    path('password_validate/<uidb64>/<token>', views.password_validate, name='password_validate'),
    path('reset_Password/', views.reset_Password, name='resetPassword'),

]