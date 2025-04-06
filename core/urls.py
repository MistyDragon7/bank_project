from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from dashboard import views as dashboard_views
from . import views

urlpatterns = [
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('loan/approve/<int:loan_id>/', dashboard_views.approve_loan, name='approve_loan'),
    path('loan/reject/<int:loan_id>/', dashboard_views.reject_loan, name='reject_loan'),
    path('transfer/', views.transfer_money, name='transfer'),
    path('loan/', views.apply_loan, name='loan'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),

]