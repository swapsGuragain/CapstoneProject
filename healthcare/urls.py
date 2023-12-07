from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tables/', views.tables, name = 'tables'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('addPatients/', views.addPatients, name = 'addPatients'),
    path('addUser/', views.addUser, name = 'addUser'),
    path('patient/<int:pk>/', views.patient, name = 'patient'),
]

