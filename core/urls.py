from django.urls import path
from . import views
from dashboard import views as dashboard_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transfer/', views.transfer_money, name='transfer'),
    path('loan/', views.apply_loan, name='loan'),
    path('register/', views.register_view, name='register'),
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),

]